"""
lesson_4_hw_1

1. Написать приложение, которое собирает основные новости с сайта на выбор
news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath.
Структура данных должна содержать:

    -название источника;
    -наименование новости;
    -ссылку на новость;
    -дата публикации.

lesson_4_hw_2
2. Сложить собранные новости в БД
"""
import time

from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

# подключаемся к БД
client = MongoClient('127.0.0.1', 27017)
# выбираем БД, если не создана - создаём
db = client['news_yandex']
collection = db.news
# Удаление коллекции
# db.drop_collection(collection)

"""Задаём headers"""
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/97.0.4692.71 Safari/537.36'}

# response = requests.get('https://yandex.ru/news/', headers=header)

# Конвертируем в дом
# dom = html.fromstring(response.text)

rubrics = [
    'personal_feed',
    'politics',
    'society',
    'business',
    'world',
    'incident',
    'culture',
    'computers',
    'science',
    'auto']
data_news = []

def request_to_yandex(str):
    try:
        time.sleep(1)
        source = f'https://yandex.ru/news/rubric/{str}'
        response = requests.get(source, headers=header)
        # params={'rubric': str},
        root = html.fromstring(response.text)
        # news_block = root.xpath("//div[contains(@class, 'mg-grid__col')]/div[contains(@class, 'mg-card')]")
        news_blocks = root.xpath("//div[contains(@class, 'mg-card mg-')]")
        return news_blocks
    except:
        print('Ошибка запроса')


count_current_news = 0
count_new_news = 0
for rubric in rubrics:
    news_block = request_to_yandex(rubric)
    count = 0
    for block in news_block:
        content_news = {}
        if count < len(news_block):
            name_source = block.xpath("//div[contains(@class, 'col mg-grid__col_xs')]/div[contains(@class, 'mg-card')]//span/a[contains(@class, '_source')]/text()")[count]
            name_news = block.xpath("//div[contains(@class, 'col mg-grid__col_xs')]/div[contains(@class, 'mg-card')]//a[contains(@class, '_link')]/text()")[count].replace('\xa0', ' ')
            link = block.xpath("//div[contains(@class, 'col mg-grid__col_xs')]/div[contains(@class, 'mg-card')]//a[contains(@class, '_link')]/@href")[count]
            date_pub = block.xpath("//div[contains(@class, 'col mg-grid__col_xs')]/div[contains(@class, 'mg-card')]//span[contains(@class, '_time')]/text()")[count]

            # название источника
            content_news['name_source'] = name_source
            # наименование новости
            content_news['name_news'] = name_news
            # ссылка на новость
            content_news['link'] = link
            # дата публикации
            content_news['date_pub'] = date_pub
            data_news.append(content_news)
            news_find = collection.find({})
            # Запись новых новостей в БД
            flag = 0
            el_id = []
            for item in news_find:
                # print(item['_id'])
                el_id.append(item['link'])
            # if flag == 0:
            if content_news['link'] in el_id:
                count_current_news += 1
                # flag = 1
            else:
                count_new_news += 1
                collection.insert_one(content_news)
            count += 1

print(f'Добавлено {count_new_news} новых новостей.')
print(f'Текущих новостей {count_current_news}.')
# pprint(data_news)
"""
Результат работы программы(первые 3 из 59):
Добавлено 59 новых новостей.
Текущих новостей 0.
[{'_id': ObjectId('61f99e30ba505f66db8602ae'),
  'date_pub': '18:35',
  'link': 'https://yandex.ru/news/story/Drevnie_lyudi_razmeshhali_ochag_smaksimalnoj_polzoj_i_minimalnym_vozdejstviem_dyma--94df47eb35779c8e2c829c1af6887780?lang=ru&rubric=personal_feed&fan=1&stid=YWF2&t=1643748461&persistent_id=178455843',
  'name_news': 'Древние люди размещали очаг с максимальной пользой и '
               'минимальным воздействием дыма',
  'name_source': 'FBM.ru'},
 {'_id': ObjectId('61f99e30ba505f66db8602af'),
  'date_pub': '17:18',
  'link': 'https://yandex.ru/news/story/Obnovlyonnyj_krossover_Kia_Seltos_gotovyat_kserijnomu_vypusku--2e802f655acd69f832639e7072c506f5?lang=ru&rubric=personal_feed&fan=1&stid=wTu4UwG8N-3lnhCiAybq&t=1643748461&persistent_id=178374893',
  'name_news': 'Обновлённый кроссовер Kia Seltos готовят к серийному выпуску',
  'name_source': 'Car.ru'},
 {'_id': ObjectId('61f99e30ba505f66db8602b0'),
  'date_pub': '01:32',
  'link': 'https://yandex.ru/news/story/Glava_MID_Lavrov_Moskva_zhdet_reakcii_NATO_naposlanie_onedelimosti_bezopasnosti--4f4514b4cb5be9f11cd41e2134132a0a?lang=ru&rubric=personal_feed&fan=1&stid=s9dMcPR3-XdrfAS6nkCv&t=1643748461&persistent_id=178501212',
  'name_news': 'Глава МИД Лавров: Москва ждет реакции НАТО на послание о '
               'неделимости безопасности',
  'name_source': 'РИА Новости'},

"""