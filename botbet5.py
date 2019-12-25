import requests
import telebot
import urllib.request
import re
import docx
import datetime
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests_html import HTMLSession
from telebot import types

token = '705618645:AAHMT7Pn1qTnvnajzvGEeCuLO5fmSTGQa8M'
bot = telebot.TeleBot(token)
all_urls = []
all_links = []
all_text = []
all_info = []
s = requests.Session()
day = ''


def curday():
    global day
    nowday = datetime.datetime.now()
    day = str(nowday.month) + '/' + str(nowday.day)


def urls():
    global all_urls
    all_urls.append('https://meduza.io/')


def find():
    global all_links
    global all_text
    curday()
    urls()
    session = HTMLSession()
    for url in all_urls:
        if url == 'https://meduza.io/':
            html = session.get(url)
            bs = BeautifulSoup(html.text)
            first = bs.find('section', {'class': 'Grid-container'})
            print(first)
            second = link_list.find_all('a')
            for item in second:
                link = item.get('href')
                if day in str(link):
                    text = item.text
                    all_links.append(link)
                    all_text.append(text)
    for url1 in all_urls:
        html = session.get(url1)
        bs = BeautifulSoup(html.text)
        one = bs.find('div', {'class': 'Toolbar-root'})
        two = one.find('span', {'class': 'ToolbarButton-text'})
        text = two.text
        all_info.append(text)


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == 'го':
        find()
        for i in range(len(all_links)):
            a = str(all_urls[i]) + str(all_text) + str(all_info)
            bot.send_message(chat_id, a)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
