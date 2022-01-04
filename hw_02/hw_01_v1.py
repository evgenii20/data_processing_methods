"""
lesson_2_hw_01

Необходимо собрать информацию о вакансиях на вводимую должность (используем
input или через аргументы получаем должность) с сайтов HH(обязательно) и/или
Superjob(по желанию). Приложение должно анализировать несколько страниц
сайта (также вводим через input или аргументы). Получившийся список должен
содержать в себе минимум:

    -Наименование вакансии.
    -Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и
    валюта. цифры преобразуем к цифрам).
    -Ссылку на саму вакансию.
    -Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). 
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с 
помощью dataFrame через pandas. Сохраните в json либо csv.

"""
import re
import time

import requests
# Для обработки HTML
from bs4 import BeautifulSoup
import json
from pprint import pprint
import pandas as pd

# url = 'https://hh.ru/search/vacancy?clusters=true&area=113&ored_clusters=true&enable_snippets=true&salary=&text=python&page=1&hhtmFrom=vacancy_search_list'
# url = 'https://hh.ru'

# https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&text=python&page=1&hhtmFrom=vacancy_search_list


"""Задаём headers"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36'}


def parser_hh(url, vacancy):
    """
    'area': '113' - Россия
    salary - зарплата
    """
    params = {'area': '113',
              'text': vacancy,
              'page': 0,
              'hhtmFrom': 'vacancy_search_list'}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    # html_page
    soup = BeautifulSoup(response.text, 'html.parser')
    # vacancy-serp-item vacancy-serp-item_premium
    page_all = soup.find_all('div', {'class': 'pager'})

    data_vacancy = []
    vacancys_list = []
    
    for page in page_all:
        #     count += 1
        page_data = {}
        # # info = page_all.find('span').next_sibling.text
        tag_a = page.find_all('a')
        max_page = 0
        for el in tag_a:
            # p1 = el.text
            if el.text != 'дальше':
                max_page = el.text
            # else:
            #     print(max_page)
        # total_page = max(int(tag_a))
        # parent_a = tag_a.parent.parent
        # # page = info.find_all('span', {'class': ''})
        # one_page = info.text
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

                # for item in vacancy_items:
                # data_vacancy.append(parser_item_hh(item))
                # print(vacancy_items)
                # pages_list.append(page_data)
                # pages = page
                # pages_list.append(page)

                # info = page.find('a', {'class': 'bloko-button'})
                # pages = info.text

                # print(f'pages_list: {pages_list}')
                # # else:
                # #     break
                # # ищем нужную карточку(и) на странице
                # vacancys = soup.find_all('div', {'class': 'vacancy-serp-item'})
                
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
                    # genre = vacancy.find('span', {'class': 'selection-film-item-meta__meta-additional-item'}).next_sibling.text
                    salary = vacancy_item.find('div', {'class': 'vacancy-serp-item__sidebar'})

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
                        valuta = (vacancy_item.find('div', {'class': 'vacancy-serp-item__sidebar'
                                                            }).text.replace(u'\u202f', u'').split())[-1]
                        salaries = salary.text.replace(u'\u202f', u'').split('-')
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
                            # for isol in range(len(salaries)):
                            sal_tmp = re.sub(r'[^0-9]', '', salaries[isol])
                            tmp.append(sal_tmp)
                            salary_min, salary_max = tmp
                            # salary_max = tmp[1]
                        else:
                            salary_max = None
                        
                    vacancy_data['name'] = name
                    vacancy_data['salary_min'] = salary_min
                    vacancy_data['salary_max'] = salary_max
                    vacancy_data['valuta'] = valuta
                    vacancy_data['link'] = link
                    vacancy_data['site'] = url
                    vacancy_data['company'] = company

                    vacancys_list.append(vacancy_data)
        time.sleep(0.25)
    pprint(vacancys_list)
    return vacancys_list


# пишем интересующую вакансию
# vacancy = input(f'Введите название интересующей вакансии: ')
VACANCY = 'Python'
URL = 'https://hh.ru'

data_frame = parser_hh(URL, VACANCY)

with open('hh.json', 'w') as hh:
    json.dump(data_frame, hh)
df = pd.read_json('hh.json')
print(df)
