# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
#   Для парсинга использовать XPath. Структура данных должна содержать:
#     название источника;
#     наименование новости;
#     ссылку на новость;
#     дата публикации.
# 2. Сложить собранные данные в БД
#
# Минимум один сайт, максимум - все три


from pprint import pprint

import requests
from lxml import html
from pymongo import MongoClient

url = 'https://lenta.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.93 Safari/537.36'
}

response = requests.get(url, headers=headers)
document = html.fromstring(response.text)

items = document.xpath('//time[@class="g-time"]')

news = [{
            'link': f"{url}{item.xpath('./../@href')[0]}",
            'name': item.xpath('./../text()')[0].replace('\xa0', ' '),
            'source': url,
            'date': item.xpath('./@datetime')[0],
        } for item in items]

client = MongoClient('127.0.0.1', 27017)
db = client['lenta']
news_collection = db['news']

for data in news:
    news_collection.update_one(
        {'link': data['link']},
        {'$set': data},
        upsert=True)

    pprint(data)
