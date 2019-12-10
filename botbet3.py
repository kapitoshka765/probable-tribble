import requests
import telebot
import urllib.request
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

token = '790148299:AAFRAXTGp1SoWhQW_FxhOWqBBgxEH43ZAuY'
bot = telebot.TeleBot(token)
url = 'https://habr.com/ru/post/280238/'
all_links = []
domain = 'https://drive.google.com/'
s = requests.Session()



def find(message):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'lxml')
    links = bs.find('div', {'class': 'BlockContent-body'}).findAll('a')
    for link in links():
        all_links.append(link)


def find_urls():
    global all_links
    response = requests.get(url)
    response.status_code
    return response.text


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == 'go':
        find(message)
        bot.send.message(chat_id, str(all_links))

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
