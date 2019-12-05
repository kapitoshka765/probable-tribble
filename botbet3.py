import requests
import telebot
import urllib3
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

token = '790148299:AAFRAXTGp1SoWhQW_FxhOWqBBgxEH43ZAuY'
bot = telebot.TeleBot(token)
url = 'http://lyceum-kungur.ru/%d0%b8%d0%b7%d0%bc%d0%b5%d0%bd%d0%b5%d0%bd%d0%b8%d1%8f-%d0%b2-' \
      '%d1%80%d0%b0%d1%81%d0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b8/'
all_links = []
domain = 'https://drive.google.com/'


def find_urls():
    global all_links
    page = urllib3.PoolManager()
    response = page.request('GET', url)
    soup = BeautifulSoup(response, 'html.parser')
    for i in soup.findAll('a', attrs={'href': re.compile('^http://')}):
        all_links.append(i.get('href'))
    if len(all_links) >= 28:
        all_links = []


@bot.message_handler(content_types=['text'])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == 'go':
        find_urls()
        bot.send_message(chat_id, all_links)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
