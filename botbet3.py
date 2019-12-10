import requests
import telebot
import urllib.request
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from requests_html import HTMLSession

token = '790148299:AAFRAXTGp1SoWhQW_FxhOWqBBgxEH43ZAuY'
bot = telebot.TeleBot(token)
url = 'http://lyceum-kungur.ru/%d0%b8%d0%b7%d0%bc%d0%b5%d0%bd%d0%b5%d0%bd%d0%b8%d1%8f-%d0%b2-%d1%80%d0%b0%d1%81%' \
      'd0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b8/'
all_links = []
domain = 'https://drive.google.com/'
s = requests.Session()



def find(message):
    session = HTMLSession()
    html = session.get(url)
    bs = BeautifulSoup(html.text)
    link_list = bs.find('div', {'class': 'BlockContent'})
    print(link_list)
    items = link_list.find_all('a')
    for item in items:
        link = item.get('href')
        bot.send_message(message.chat.id, str(link))

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
