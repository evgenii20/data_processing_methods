"""
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

import requests
import json

url = 'https://cloud-api.yandex.net/v1/'
token = 'token'

headers = {
    'Content-Type': 'application/json',
    'Authorization': token
}

disk_info = 'disk'
folder_info = 'disk/resources'
# folder_info = 'disk/ResourceList'

# Ответ 401
disk = requests.get(f'{url}{disk_info}')
print(disk.json())
"""
Ответ сервера на запрос "get":
{'message': 'Не авторизован.', 'description': 'Unauthorized', 'error': 'UnauthorizedError'}
"""

disk = requests.get(f'{url}{disk_info}', headers=headers)
# disk = requests.get(f'{url}{folder_info}', headers=headers)

# записываем полученные данные в json-файл
with open('data_hw_02.json', 'w') as f:
    json.dump(disk.json(), f)
print(disk.json())

# disk1 = requests.get(f'{url}{folder_info}?path=app:/', headers=headers)

# https://cloud-api.yandex.net/v1/disk/resources/files
# disk1 = requests.get(f'{url}{folder_info}{files}', data=payload, headers=headers)
# disk1 = requests.get(f'{url}{folder_info}?path=/&ResourceList{fields}', headers=headers)

# получаем ответ на запрос:
disk = requests.get(f'{url}{folder_info}?path=/&ResourceList', headers=headers)
# проверяем
print(disk.json())
# Названия файлов в папке

# for i in disk.json()['_embedded']['items']['path']:
# for i in disk1.json()['path']:

# записываем новые данные в json-файл
with open('data_hw_02.json', 'w') as f:
    # dumps = json.dump(disk.json(), f)
    json.dump(disk.json(), f)

# читаем файл
with open('data_hw_02.json', 'r') as f:
    files = json.load(f)


for i in files['_embedded']['items']:
    temp = i['path'].split('/')
    # temp = (tmp[1])
    # print(temp[1])
    # print(i)
    # print(i['name'])
    print(temp[1])

"""
Полученный список папок и файлов яндекс диска:
Загрузки
Клипы
Книги
Музыка
Приложения
фото
Горы.jpg
Зима.jpg
Мишки.jpg
Море.jpg
Москва.jpg
Санкт-Петербург.jpg
"""
