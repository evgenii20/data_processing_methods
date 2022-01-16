"""
lesson_3_hw_1

1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
реализовать функцию, которая будет добавлять только новые вакансии/продукты в
вашу базу.

"""
import re
import time
from pprint import pprint

import requests
# Для обработки HTML
from bs4 import BeautifulSoup
from pymongo import MongoClient

# import json
# from pprint import pprint
# import pandas as pd


# подключаемся к БД
client = MongoClient('127.0.0.1', 27017)
# выбираем БД, если не создана - создаём
db = client['vacancy_hh']
# создаём коллекцию, указатель на коллекцию и храним в смысловой переменной
# для проведения операций уже с указанной переменной
collection = db.vacancy
# Удаление коллекции
# db.drop_collection(collection)

"""Задаём headers"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36'}


def parser_hh(url, vacancy_text):
    """
    'area': '113' - Россия
    salary - зарплата

    """
    params = {'area': '113',
              'text': vacancy_text,
              'page': 0,
              'hhtmFrom': 'vacancy_search_list'}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    # html_page
    soup = BeautifulSoup(response.text, 'html.parser')
    # vacancy-serp-item vacancy-serp-item_premium
    page_all = soup.find_all('div', {'class': 'pager'})

    # vacancy_find = {}
    vacancys_list = []
    count_current_vacancy = 0
    count_new_vacancy = 0
    for page in page_all:
        tag_a = page.find_all('a')
        max_page = 0
        for el in tag_a:
            # p1 = el.text
            if el.text != 'дальше':
                max_page = el.text

        # получаем страницу с вакансиями
        for i in range(0, int(max_page)):
            # page_data['page'] = i
            params['page'] = i

            html = requests.get(url + '/search/vacancy', params=params, headers=headers)
            if html.ok:
                # получаем html разметку:
                # html_page = BeautifulSoup(response.text, 'html.parser'))
                html_page = BeautifulSoup(html.text, 'html.parser')
                # получаем карточку акансии
                vacancy_items = html_page.find_all('div', {'class': 'vacancy-serp-item'})

                # for vacancy in vacancys:
                for vacancy_item in vacancy_items:
                    vacancy_data = {}
                    # получаем(ищем) тег "a"
                    info = vacancy_item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
                    # info = vacancy_item.find('span', {'class': 'g-user-content'})
                    # info = vacancy_item.find('div', {'class': 'vacancy-serp-item'})
                    # записываем в переменную название вакансии
                    name = info.text
                    # link = url + info.parent.get('href')
                    # получаем ссылку на вакансию
                    link = info.get('href')
                    # Получаем id вакансии
                    id = re.search(r"\d{1,20}", link).group(0)
                    # genre = vacancy.find('span', {'class': 'selection-film-item-meta__meta-additional-item'}
                    # ).next_sibling.text
                    # salary = vacancy_item.find('div', {'class': 'vacancy-serp-item__sidebar'})
                    # salary = vacancy_item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}
                    # ).text.replace("\u202f", "").replace("\xa0", " ")
                    salary = vacancy_item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                    # vacancy_item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).contents
                    # ['300\u202f000 – 400\u202f000 ', ' ', 'руб.']

                    company = vacancy_item.find('div', {'class': 'vacancy-serp-item__meta-info-company'
                                                        }).text.replace(u'\xa0', u' ')
                    # строка ниже для тестирования:
                    # salary = '150 000 – 190 000 руб.'
                    # salary = vacancy_item.find('span', {'class': ['bloko-header-section-3',
                    #                                               'bloko-header-section-3_lite']})
                    if not salary or salary.text == '':
                        # для тестирования
                        # if not salary or salary == '':
                        salary_min = None
                        salary_max = None
                        valuta = None
                    else:
                        # старые данные по unicode
                        # salary = salary.getText().replace(u'\xa0', u'')
                        # новые данные:
                        # salary = salary.getText().replace(u'\u202f', u'')
                        # salary = salary.text.replace(u'\u202f', u'').split()
                        # salaries = salary.text.replace(u'\u202f', u'').split()

                        try:
                            valuta = (vacancy_item.find('div', {'class': 'vacancy-serp-item__sidebar'}).text.replace(u'\u202f', u'').split())[-1]
                        except AttributeError:
                            valuta = None

                        salary = vacancy_item.find('span',
                                                   {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.replace(
                            "\u202f", "").replace("\xa0", " ").replace(' \u2013', '').split()
                        # salaries = salary.text.replace(u'\u202f', u'').split('-')
                        # salaries = salary.text.replace(u'\u202f', u'').split('-')
                        # salaries = salary.text.split(u'-')
                        salaries = salary
                        # для тестирования:
                        # salary_repl = salary.replace(u'\u202f', u'')
                        # salary = salary_repl

                        if len(salaries) == 1:
                            salaries[0] = re.sub(r'[^0-9]', '', salaries[0])
                            salary_min = int(salaries[0])

                        # salaries = salary.split(' - ').replace(u'\xa0', u'')
                        # salaries = salary.split(' \u2013 ')
                        if len(salaries) > 1:
                            tmp = []
                            # type(salaries) -> list
                            isol = 0
                            # count = 0
                            for isol in range(len(salaries)):
                                sal_tmp = re.sub(r'[^0-9]', '', salaries[isol])
                                # if sal_tmp[isol] != '':
                                if isol < 2:
                                    tmp.append(sal_tmp)
                                    # count += 1
                                if isol == 2:
                                    valuta = salaries[isol]
                            salary_min, salary_max = tmp
                            # salary_max = tmp[1]
                        else:
                            salary_max = None

                        #     rating = vacancy.find('span', {'class': 'rating__value'}).getText()
                        #     try:
                        #         rating = float(rating)
                        #     except Exception as e:
                        #         rating = None
                        #
                    vacancy_data['_id'] = id
                    vacancy_data['name'] = name
                    vacancy_data['salary_min'] = salary_min
                    vacancy_data['salary_max'] = salary_max
                    vacancy_data['valuta'] = valuta
                    vacancy_data['link'] = link
                    vacancy_data['site'] = url
                    vacancy_data['company'] = company

                    # {'_id': '50068829',
                    #  'name': 'Team Lead Python/Django / Руководитель отдела разработки и тестирования',
                    #  'salary_min': '300000', 'salary_max': '400000', 'valuta': 'руб.',
                    #  'link': 'https://hh.ru/vacancy/50068829?from=vacancy_search_list&query=Python&hhtmFrom=vacancy_search_list',
                    #  'site': 'https://hh.ru', 'company': 'CATAPULTO.RU'}
                    # # vacancys_list.append(vacancy_data)
                    vacancy_find = collection.find({})
                    # Запись новых вакансий в БД
                    flag = 0
                    el_id = []
                    for item in vacancy_find:
                        # print(item['_id'])
                        el_id.append(item['_id'])
                    # if flag == 0:
                    if vacancy_data['_id'] in el_id:
                        count_current_vacancy += 1
                        # flag = 1
                    else:
                        count_new_vacancy += 1
                        collection.insert_one(vacancy_data)
                        # flag = 0
                    # if vacancy_data['_id'] is collection.find(vacancy_data['_id']):
                    # if vacancy_data is collection.find(vacancy_data['_id']):
                    #     count_current_vacancy += 1
                    #     # collection.update_one({'_id': vacancy_data['_id']}, {'set': vacancy_data})
                    # else:
                    #     count_new_vacancy += 1
                    #     collection.insert_one(vacancy_data)
                    # item

        time.sleep(0.25)
    print(f'Добавлено {count_new_vacancy} новых вакансий.')
    print(f'Текущих вакансий {count_current_vacancy}.')
    # Добавлено 800 новых вакансий.

    #     vacancys_list.append(vacancy_data)
    # print()
    # pprint(vacancys_list)
    # return vacancys_list


# def filter_unicod(data):
#     # char_list = ['\u200e', '\u0138', '\u200c', '\u202f', '\xa0']
#     char_list = ['\u200e', '\u200c', '\u202f', '\xa0']
#     right_data = data
#     for char in char_list:
#         if char == '\xa0':
#             right_data = right_data.replace(char, ' ')
#         else:
#             right_data = right_data.replace(char, '')
#     return right_data


# пишем интересующую вакансию
# vacancy = input(f'Введите название интересующей вакансии: ')
VACANCY_TXT = 'Python'
URL = 'https://hh.ru'
# url_superjob = 'https://www.superjob.ru'

parser_hh(URL, VACANCY_TXT)
# data_frame = parser_hh(URL, VACANCY_TXT)

# with open('hh.json', 'w') as hh:
#     json.dump(data_frame, hh)
# df = pd.read_json('hh.json')
# print(df)
