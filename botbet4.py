import telebot
from telebot import types

token = '771996310:AAEK1JCyG00t7XCBDGbzSc9FEPexsd7oiCo'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        '''Мы рады, что вы с нами.''',
        reply_markup=keyboard())

@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    worth = 20
    if message.text == 'Make min bet':
        text = 'Minimum bet placed' \
               'Current worth is' + ' ' + str(worth)
        bot.send_message(chat_id, text, reply_markup=keyboard())
        worth += 20
    if message.text == 'Make bet':
        text = 'How much do you want to bet?'
        bot.send_message(chat_id, text, reply_markup=force)
        worth += int(message.text)


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('Make min bet')
    markup.add(button1)
    return markup

def force():
    force_markup = types.ForceReply()
    tb.send_message(chat_id, 'Choose your bet', reply_markup=force_markup)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)