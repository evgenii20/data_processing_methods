"""
lesson_3_hw_2

2. Написать функцию, которая производит поиск и выводит на экран
вакансии с заработной платой больше введённой суммы (необходимо
анализировать оба поля зарплаты). Для тех, кто выполнил задание с
Росконтролем - напишите запрос для поиска продуктов с рейтингом не
ниже введенного или качеством не ниже введенного (то есть цифра
вводится одна, а запрос проверяет оба поля)

"""
from pprint import pprint
from pymongo import MongoClient


def vacancy_filter_salary(salaries):
    """
    Структура данных:
    vacancy_data['_id'] = id
    vacancy_data['name'] = name
    vacancy_data['salary_min'] = salary_min
    vacancy_data['salary_max'] = salary_max
    vacancy_data['valuta'] = valuta
    vacancy_data['link'] = link
    vacancy_data['site'] = url
    vacancy_data['company'] = company"""

    # подключаемся к БД
    client = MongoClient('127.0.0.1', 27017)
    # выбираем БД, если не создана - создаём
    db = client['vacancy_hh']
    # создаём коллекцию, указатель на коллекцию и храним в смысловой переменной
    # для проведения операций уже с указанной переменной
    collection = db.vacancy

    vacancy_find = collection.find({"$or": [{'salary_min': {'$lte': salaries}}, {'salary_max': {'$gte': salaries}}]})
    # vacancy_find = collection.find({})
    count = 0
    for el in vacancy_find:
        # print()
        count += 1
        pprint(el['_id'])
        pprint(el['name'])
        pprint(el['salary_min'])
        pprint(el['salary_max'])
        pprint(el['valuta'])
        pprint(el['link'])
        pprint(el['site'])
        pprint(el['company'])

    print(f'Подходящих вакансий {count}.')
    # Добавлено 800 новых вакансий.


# vacancy = input(f'Введите название интересующей вакансии: ')

try:
    salary = input(f'Введите желаемый уровень зарплаты:\n')
    # salary = '100000'
except Exception:
    print(f'Необходимо ввести целое число, например: 100000\n')

vacancy_filter_salary(salary)
