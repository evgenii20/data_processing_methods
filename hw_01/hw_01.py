"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
пользователя, сохранить JSON-вывод в файле *.json.
"""

import requests
import json

# headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
#            'Authorization': 'Basic cG9zdG1hbjpwYXNzd29yZA=='}
#
# # req = requests.get("https://yandex.ru")
# req = requests.get('https://postman-echo.com/basic-auth', headers=headers)
# print('Заголовки: \n', req.headers)
# print('Ответ: \n', req.text)

url = 'https://api.github.com'
user = 'opencart'

# Получаем ответ на "get" запрос
response = requests.get(f'{url}/users/{user}/repos')

# записываем полученные данные в json-файл
with open('data_hw_01.json', 'w') as f:
    json.dump(response.json(), f)

# обрабатываем полученные данные и выводим результат
for i in response.json():
    print(i['name'])
