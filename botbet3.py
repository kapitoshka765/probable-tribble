import requests
import telebot
import urllib.request
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

token = '790148299:AAFRAXTGp1SoWhQW_FxhOWqBBgxEH43ZAuY'
bot = telebot.TeleBot(token)
url = 'http://lyceum-kungur.ru/%d0%b8%d0%b7%d0%bc%d0%b5%d0%bd%d0%b5%d0%bd%d0%b8%d1%8f-%d0%b2-' \
      '%d1%80%d0%b0%d1%81%d0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b8/'
all_links = []
domain = 'https://drive.google.com/'
s = requests.Session()



def find(message):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'lxml')
    links = bs.find('div', {'class': 'BlockContent-body'}).findAll('a')
    for link in links():
        bot.send.message(message.chat.id, link)


def find_urls():
    global all_links
    response = requests.get(url)
    response.status_code
    return response.text


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == 'go':
        bs = BeautifulSoup(find_urls(), 'lxml')
        links = bs.find('div,'{'class' : 'BlockContent-body'}).findAll('a')
        for link in links:
            bot.send.message(chat_id, link)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
