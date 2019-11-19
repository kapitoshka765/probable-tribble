import telebot
from telebot import types

token = '771996310:AAEK1JCyG00t7XCBDGbzSc9FEPexsd7oiCo'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        'Мы рады, что вы с нами.',
        reply_markup=keyboard())


@bot.message_handler(content_types=['text'])
def send_anytext(message,):
    global worth
    chat_id = message.chat.id
    if message.text == 'Make min bet':
        text = 'Minimum bet placed' \
               'Current worth is' + ' ' + str(worth)
        bot.send_message(chat_id, text, reply_markup=keyboard())
        worth += 20
    elif message.text == 'Make bet':
        text = 'How much do you want to bet?'
        force_markup = types.ForceReply()
        bot.send_message(chat_id, 'Choose your bet', reply_markup=force_markup)
    elif isint(message.text):
        worth += int(message.text)
        bot.send_message(chat_id, 'Your bet was placed', reply_markup=keyboard())


worth = 0


def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('Make min bet')
    button2 = types.KeyboardButton('Make bet')
    markup.add(button1, button2)
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
