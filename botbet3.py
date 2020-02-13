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

token = '790148299:AAFRAXTGp1SoWhQW_FxhOWqBBgxEH43ZAuY'
bot = telebot.TeleBot(token)
url = 'http://lyceum-kungur.ru/%d0%b8%d0%b7%d0%bc%d0%b5%d0%bd%d0%b5%d0%bd%d0%b8%d1%8f-%d0%b2-%d1%80%d0%b0%d1%81%' \
      'd0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b8/'
all_links = []
all_text = []
all_ids =[]
all_days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'cуббота']
domain = 'https://drive.google.com/'
s = requests.Session()


def find():
    global all_links
    global all_text
    session = HTMLSession()
    html = session.get(url)
    bs = BeautifulSoup(html.text)
    link_list = bs.find('div', {'class': 'entry'})
    print(link_list)
    items = link_list.find_all('a')
    if len(all_links) > len(all_text) or len(all_text) > len(all_links):
        all_links = []
        all_text = []
    for item in items:
        link = item.get('href')
        text = item.text
        if link not in all_links:
            all_links.append(link)
        if text not in all_text:
            all_text.append(text)


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    if chat_id not in all_ids:
        all_ids.append(chat_id)
    if message.text == 'Расписание':
        find()
        bot.send_message(chat_id, 'Выберите нужный день', reply_markup=days())
    if message.text == 'Другое':
        find()
        bot.send_message(chat_id, 'Выберите нужный пункт', reply_markup=another())
    if message.text in all_text:
        a = message.text
        aa = all_text.index(a)
        bot.send_message(chat_id, str(all_links[aa]), reply_markup=starting())
    if message.text == 'krism id':
        bot.send_message(chat_id, len(all_ids), reply_markup=starting())
    if message.text == 'krism send':
        for i in all_ids:
            bot.send_message(i, message.text, reply_markup=starting())
    elif all_days.count(message.text) and message.text != 'Расписание' and message.text != 'Другое':
        bot.send_message(chat_id, 'Такой команды не существует, выберите одну, нажав на 4 точки', reply_markup=starting())


def starting():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    button = types.KeyboardButton('Расписание')
    button1 = types.KeyboardButton('Другое')
    markup.row(button, button1)
    return markup


def days():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    for opa in range(len(all_text)):
        if 'января (' in str(all_text[opa]) or 'февраля (' in str(all_text[opa]):
            markup.row(types.KeyboardButton(str(all_text[opa])))
    return markup


def another():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    for opa in range(len(all_text)):
        for i in range(len(all_days)):
            if all_days[i] not in str(all_text[opa]):
                markup.row(types.KeyboardButton(str(all_text[opa])))
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
