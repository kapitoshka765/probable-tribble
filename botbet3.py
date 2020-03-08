import requests
import telebot
import urllib.request
import re
import docx
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests_html import HTMLSession
from telebot import types

token = '705618645:AAHMT7Pn1qTnvnajzvGEeCuLO5fmSTGQa8M'
nuzno = '45563195'
bot = telebot.TeleBot(token)
name1 = ''
telephon1 = ''
other1 = ''
start = []
telephon = []
name = []
other =[]
need = ['89', '7 9', '+7 9', '8 9', '7 (9', '79']


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    global name1
    global telephon1
    global other1
    global other
    global start
    global telephon
    chat_id = message.chat.id
    if message.text == 'Записаться':
        ubrat()
        start.append(chat_id)
        bot.send_message(chat_id, 'Пожалуйста, введите Ваше имя и фамилию')
    elif chat_id in start:
        name1 = message.text
        start = []
        telephon.append(chat_id)
        bot.send_message(chat_id, 'Пожалуйста, введите Ваш номер телефона, по которому мы сможем с Вами связаться')
    elif chat_id in telephon:
        telephon1 = message.text
        telephon = []
        other.append(chat_id)
        bot.send_message(chat_id, 'А теперь, введите причину обращения в Amcar Service')
    elif chat_id in other:
        other1 = message.text
        bot.send_message(nuzno, 'Запись от ' + name1 + ' с телефоном ' + telephon1 + ' по причине ' + other1)
        ubrat()
        bot.send_message(chat_id, 'Спасибо за Вашш обращение, ожидайте звонка от Amcar Service')
    else:
        bot.send_message(chat_id, 'Такой команды не существует. Пожалуйста, нажмите на доступную команду в меню рядом с вашей клавиатурой', reply_markup=starting())


def ubrat():
    global start1
    global other1
    global telephon1
    global start
    global other
    global telephon
    start = []
    other = []
    telephon= []
    start1 = ''
    other1 = ''
    telephon1 = ''


def starting():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    button = types.KeyboardButton('Записаться')
    markup.row(button)
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
