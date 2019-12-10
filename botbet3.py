import requests
import telebot
import urllib.request
import re
import docx
from io import BytesIO
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
    link_list = bs.find('div', {'class': 'entry'})
    print(link_list)
    items = link_list.find_all('a')
    for item in items:
        link = item.get('href')
        all_links.append(link)

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
        for a in range(1, len(all_links)):
            if a == len(all_links):
                break
            b = all_links[a]
            docx1 = BytesIO(requests.get(b).content)
            text = docx.Document(docx1)
            table_size = len(text.tables[1].rows)
            for i in range(table_size):
                info.append(text.tables[1].rows[i].cells[1].text)
        bot.send_message(chat_id, info)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=20)
