import telebot
import time
import requests
import json
import sqlite3
import threading
from uuid import uuid4
from telebot import types
from telebot.types import LabeledPrice, ShippingOption

qiwi_acc = '89058638358'
api_access_token = 'cdd16f5f5853c4be4381216d3878d25d'
token = '771996310:AAEK1JCyG00t7XCBDGbzSc9FEPexsd7oiCo'
bot = telebot.TeleBot(token)
db = ''
ids = ''
win = 0
lot_info = ''
worth = 0
prices = [LabeledPrice(label='Pay', amount=14400)]
ok = 0
lot_text = 0


class QApi(object):

    def __init__(self, api_access_token, qiwi_acc, delay=1):
        self._s = requests.Session()
        self._inv = {}
        self._echo = None
        self.thread = False
        self.delay = delay

    @property
    def payments(self):
        return self.get_payments()

    def get_payments(self, rows=5):
        args = {
            'rows': rows,
            'operation': 'IN'
        }
        response = self._s.get(
            url='https://edge.qiwi.com/payment-history/v1/persons/%s/payments' % qiwi_acc,
            params=args
        )
        data = response.json()
        return data

    def bill(self, price, comment=uuid4(), currency=643):
        comment = str(comment)
        self._inv[comment] = {
            'price': price,
            'currency': currency,
            'success': False
        }
        return comment

    def check(self, comment):
        if comment not in self._inv:
            return False
        return self._inv[comment]['succes']

    def _async_loop(self, target):
        lock = threading.Lock()
        while self.thread:
            try:
                lock.acquire()
                target()
            finally:
                lock.release()

    def parse_payments(self):
        payments = self.payments
        if 'errorCode' in payments:
            time.sleep(10)
            return
        for payment in payments['data']:
            if payment['comment'] in self._inv:
                if payment['total']['amount'] >= self._inv[payment['comment']]['price'] and payment['total'] \
                        ['currency'] == self._inv['comment']['currency'] and not self._inv[payment['comment']] \
                        ['success']:
                    self._inv[payment['comment']]['success'] = True
                    if self._echo is not None:
                        self.echo({
                            payment['comment']: self._inv[payment['comment']]
                        })
        time.sleep(self.delay)

    def start(self):
        if not self.thread:
            self.thread = True
            th = threading.Thread(target=self._async_loop, args=(self.parse_payments,))
            th.start()

    def stop(self):
        self.thread = False


@bot.message_handler(commands=['pay'])
def command_pay(message):
    global api_access_token
    global qiwi_acc
    api = QApi(api_access_token=api_access_token, qiwi_acc=qiwi_acc)
    price = 1
    comment = api.bill(price)
    bot.send_message(message.chat.id, "Переведите %i рублей на счет %s c комментарием %s" % (price, qiwi_acc, comment))
    api.start()
    while True:
        if api.check(comment):
            bot.send_message(message.chat.id, 'Платеж получен')
            break
        sleep(1)


@bot.message_handler(content_types=['succesful_payment'])
def got_payment(message):
    global worth
    bot.send_message(message.chat.id,
                     'Оплата прошла успешно, в скором времени вам поступить предложение обмена в Steam')
    worth = 0


def start(name, value, url, games, pages, photo):
    return 'Номер лота:' + name + ' ' + 'Стоимость предметов на первой странице:' + value + 'руб. ' \
           + 'Ссылка на аккаунт:' + url + ' ' + 'Игры на аккаунте:' + games + ' ' + 'Страниц инвентаря:' + pages \
           + photo


def add_lot(message):
    global lot_text
    global lot_info
    lot_info = str(message.text[5:])
    lot_info = lot_info.split(', ')
    lot_text = start(*lot_info)
    bot.send_message(message.chat.id, 'Completed')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global db
    db = db + '|' + str(message.chat.id)
    bot.send_message(
        message.chat.id,
        'Мы рады, что вы с нами. Минимальная ставка составляет 20',
        reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    global worth
    global token
    global ok
    global lot_text
    global db
    global ids
    global win
    global lot_info
    chat_id = message.chat.id
    if message.text[:4] == '/add':
        add_lot(message)
        ok = 1
        ids = db[1:].split('|')
        for x in range(len(ids)):
            bot.send_message(ids[x], lot_text)
    elif message.text == 'krism end':
        ok = 0
        bot.send_message(chat_id, 'Completed')
        bot.send_message(win, 'Вы выйграли этот аукцион под номером' + str(lot_info[:1]) + '. Теперь вам необходимо \
                         оплатить ваш заказ, для этого введите команду /pay')
    elif message.text == 'Минимальная ставка' and ok == 1:
        worth += 20
        text = 'Минимальная ставка поставлена.' + ' ' + 'На данный момент текущая стоимость' + ' ' + str(worth)
        win = message.chat.id
        bot.send_message(chat_id, text, reply_markup=keyboard())
    elif message.text == 'Ставка' and ok == 1:
        force_markup = types.ForceReply()
        bot.send_message(chat_id, 'Выберите вашу ставку', reply_markup=force_markup)
    elif isint(message.text) and ok == 1:
        if int(message.text) > 20 and int(message.text) > worth:
            worth = int(message.text)
            textisint = 'Ваша ставка была поставлена. ' + 'Текущая стоимость' + ' ' + str(worth)
            win = message.chat.id
            bot.send_message(chat_id, textisint, reply_markup=keyboard())
        else:
            bot.send_message(chat_id, 'Ваша ставка меньше минимальной, попробуйте снова', reply_markup=keyboard())
    elif message.text == 'Текущая стоимость' and ok == 1:
        bot.send_message(chat_id, str(worth), reply_markup=keyboard())
    elif message.text == 'krism zero' and ok == 1:
        worth = 0
        bot.send_message(chat_id, 'Completed', reply_markup=keyboard())


def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton('Минимальная ставка')
    button2 = types.KeyboardButton('Ставка')
    button3 = types.KeyboardButton('Текущая стоимость')
    markup.row(button1, button2)
    markup.row(button3)
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
