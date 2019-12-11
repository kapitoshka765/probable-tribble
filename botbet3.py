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
domain = 'https://drive.google.com/'
s = requests.Session()
aa = 0



def find(message):
    session = HTMLSession()
    html = session.get(url)
    bs = BeautifulSoup(html.text)
    link_list = bs.find('div', {'class': 'entry'})
    print(link_list)
    items = link_list.find_all('a')
    for item in items:
        link = item.get('href')
        text = item.get_text
        if link not in all_links:
            all_links.append(link)
        if text not in all_text:
            all_text.append(text)

def find_urls():
    global all_links
    response = requests.get(url)
    return response.text


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == 'go':
        info = []
        find(message)
        bot.send_message(chat_id, '', reply_markup=keyboard())
    if message.text in all_text:
        aa = all_text.find(message)
        bot.send_message(chat_id, str(all_links[aa]))

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
    for opa in range(len(all_text)):
        markup.row(types.KeyboardButton(all_text[opa]))
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
