import telebot
import time
from telebot import types

token = '771996310:AAEK1JCyG00t7XCBDGbzSc9FEPexsd7oiCo'
bot = telebot.TeleBot(token)


def auc_time():
    global token
    hour = 60
    ok = 1
    time.sleep(hour)
    ok = 0


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        'Мы рады, что вы с нами. Минимальная ставка составляет 20',
        reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    global worth
    global token
    chat_id = message.chat.id
    ok = 0
    if message.text == 'krism start':
        auc_time()
    elif message.text == 'Минимальная ставка' and ok == 1:
        worth += 20
        text = 'Минимальная ставка поставлена.' + ' ' + 'На данный момент текущая стоимость' + ' ' + str(worth)
        bot.send_message(chat_id, text, reply_markup=keyboard())
    elif message.text == 'Ставка' and ok == 1:
        text = 'Сколько вы хотите поставить??'
        force_markup = types.ForceReply()
        bot.send_message(chat_id, 'Выберите вашу ставку', reply_markup=force_markup)
    elif isint(message.text) and ok == 1:
        if int(message.text) > 20 and int(message.text) > worth:
            worth = int(message.text)
            textisint = 'Ваша ставка была поставлена.' + 'Текущая стоимость' + ' ' + str(worth)
            bot.send_message(chat_id, textisint, reply_markup=keyboard())
        else:
            bot.send_message(chat_id, 'Ваша ставка меньше минимальной, попробуйте снова', reply_markup=keyboard())
    elif message.text == 'Текущая стоимость' and ok == 1:
        bot.send_message(chat_id, str(worth), reply_markup=keyboard())
    elif message.text == 'krism zero' and ok == 1:
        worth = 0
        bot.send_message(chat_id, 'Completed', reply_markup=keyboard())


worth = 0


def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('Минимальная ставка')
    button2 = types.KeyboardButton('Ставка')
    button3 = types.KeyboardButton('Текущая стоимость')
    markup.add(button1, button2, button3)
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
