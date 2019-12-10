import requests
import telebot
import urllib.request
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests_html import HTMLSession

token = '790148299:AAFRAXTGp1SoWhQW_FxhOWqBBgxEH43ZAuY'
bot = telebot.TeleBot(token)
url = 'https://habr.com/ru/post/280238/'
all_links = []
domain = 'https://drive.google.com/'
s = requests.Session()



def find(message):
    session = HTMLSession()
    html = session.get(url)
    bs = BeautifulSoup(html.text, 'lxml')
    links = bs.find('div', {'class': 'content-list'}).find('a').get('href')
    for i in links():
        i = i.find('a')
        for x in i():
            x = x.get('href')
            bot.send.message(message.chat.id, str(x))


def find_urls():
    global all_links
    response = requests.get(url)
    return response.text


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == 'go':
        find(message)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
