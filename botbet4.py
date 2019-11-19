import telebot
from telebot import types

token = '771996310:AAEK1JCyG00t7XCBDGbzSc9FEPexsd7oiCo'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        'Мы рады, что вы с нами. Минимальная ставка составляет 20',
        reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def send_anytext(message, ):
    global worth
    chat_id = message.chat.id
    if message.text == 'Минимальная ставка':
        worth += 20
        text = 'Минимальная ставка поставлена' \
               'На данный момент стоимость' + ' ' + str(worth)
        bot.send_message(chat_id, text, reply_markup=keyboard())
    elif message.text == 'Ставка':
        text = 'Сколько вы хотите поставить??'
        force_markup = types.ForceReply()
        bot.send_message(chat_id, 'Выберите вашу ставку', reply_markup=force_markup)
    elif isint(message.text):
        if int(message.text) > 20:
            worth += int(message.text)
            bot.send_message(chat_id, 'Ваша ставка была поставлена', reply_markup=keyboard())
        else:
            bot.send_message(chat_id, 'Ваша ставка меньше минимальной, попробуйте снова', reply_markup=keyboard())


worth = 0
if worth > 1000:
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
    markup.add(button1, button2)
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
