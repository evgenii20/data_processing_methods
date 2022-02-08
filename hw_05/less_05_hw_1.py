"""
Вариант I

Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить
данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#
"""
import re
from pprint import pprint

from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import time

# подключаемся к БД
client = MongoClient('127.0.0.1', 27017)
# выбираем БД, если не создана - создаём
db = client['mail']
collection = db.mail
# Удаление коллекции
# db.drop_collection(collection)

# Устанавливаем опции открытия окна
chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='../chromedriver.exe', options=chrome_options)
driver.implicitly_wait(30)
# Переходим на сайт
driver.get('https://mail.ru/')

elem = driver.find_element(By.NAME, "login")
# Ввод данных
elem.send_keys("study.ai_172@mail.ru")
elem = driver.find_element(By.ID, "saveauth")
elem.click()

button = driver.find_element(By.XPATH, "//button[contains(text(),'Ввести пароль')]")
button.click()

elem = driver.find_element(By.NAME, "password")
# Ввод данных
elem.send_keys(f"NextPassword172#")
elem.send_keys(Keys.ENTER)

time.sleep(5)
select_all = driver.find_element(By.XPATH, "//span[@class='button2__wrapper']/..")
select_all.click()

mail_count = driver.find_elements(By.XPATH, "//span[contains(@class, 'button2_select-all')]/span")[0].text.split('\n')[0]
time.sleep(3)
select_all = driver.find_element(By.XPATH, "//span[@class='button2__wrapper']/..")
select_all.click()

scroll = driver.find_element(By.XPATH, "//div[@class='ReactVirtualized__Grid__innerScrollContainer']")
# scroll.send_keys(Keys.ESCAPE)
mail_url = []
# Получаем ссылку на письмо
count = 0
mail_url_set = set()
while len(mail_url_set) < int(mail_count):
    try:

        elem = driver.find_elements(By.XPATH, "//a[contains(@class, 'js-tooltip-direction_letter-bottom')]")
        for el in elem:
            mail_url.append(el.get_attribute('href'))
            mail_url_set = set(mail_url)
            count += 1

        el.send_keys(Keys.ESCAPE)
        scroll.send_keys(Keys.PAGE_DOWN)
        if elem == None:
            break
        # print(count)
    except ElementNotInteractableException:
        continue

mail_list = []
for item in mail_url_set:
    driver.get(item)
    mail_data = {}
    # id атрибута
    id = int(re.findall(r':\d+:', item)[0][1:-2])
    # Тема письма
    subject = driver.find_element(By.XPATH, "//div[contains(@class, 'thread__subject-line')]").text
    # От кого
    author = driver.find_element(By.XPATH, "//div[@class='letter__author']/span").text
    # Дата отправки
    dates = driver.find_element(By.XPATH, "//div[@class='letter__author']/div[@class='letter__date']").text
    # Текст письма полный
    text_mail = driver.find_element(By.XPATH, "//div[@class='letter__body']").text

    mail_data['_id'] = id
    mail_data['subject'] = subject
    mail_data['author'] = author
    mail_data['dates'] = dates
    mail_data['text_mail'] = text_mail

    mail_list.append(mail_data)
    collection.insert_one(mail_data)
    # Выход из письма
    ActionChains.send_keys(Keys.ESCAPE)

pprint(mail_list)
driver.quit()
