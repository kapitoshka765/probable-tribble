import telebot
import time
from telebot import types
from telebot.types import LabeledPrice, ShippingOption

provider_token = '381764678:TEST:12609'
token = '771996310:AAEK1JCyG00t7XCBDGbzSc9FEPexsd7oiCo'
bot = telebot.TeleBot(token)
db = ''
ids = ''
win = 0
lot_info = ''
worth = 0
prices =[LabeledPrice(label='Pay', amount=14400)]
ok = 0
lot_text = 0


@bot.message_handler(commands=['pay'])
def command_pay(message):
    bot.send_message(message.chat.id, 'Теперь вам необходимо оплатить ваш выйгрыш')
    bot.send_invoice(message.chat.id, title='Paying your order',
                     description='Вам необходимо оплатить ваш заказ',
                     provider_token=provider_token,
                     currency='RUB',
                     photo_url='https://sun9-19.userapi.com/c844720/v844720812/a82fe/pmX3mALvvW0.jpg',
                     photo_height=512,
                     photo_width=512,
                     photo_size=512,
                     is_flexible=False,
                     prices=prices,
                     invoice_payload='Pay',
                     start_parameter='steam-auc-bot')


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
