"""
Вариант II

2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo
и складывает данные в БД. Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары
"""
from pprint import pprint

from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# подключаемся к БД
client = MongoClient('127.0.0.1', 27017)
# выбираем БД, если не создана - создаём
db = client['mvideo']
collection = db.mvid
# Удаление коллекции
# db.drop_collection(collection)

# Устанавливаем опции открытия окна
chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='../chromedriver.exe', options=chrome_options)
# Переходим на сайт
driver.get('https://www.mvideo.ru/')

# Ищем кнопку "В тренде", поднимаемся к родителю, это тег button и делаем клик
elem = driver.execute_script("window.scrollTo(0, 1600)")
# Ждём в течении 30 сек.
wait = WebDriverWait(driver, 30)
# button = driver.find_element(By.XPATH, "//span[contains(text(),'В тренде')]/../..")
button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'В тренде')]/../..")))
button.click()
time.sleep(1)
block_carts = driver.find_elements(By.TAG_NAME, 'mvid-product-cards-group')[1]
scroll = block_carts.find_element(By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted']//div[@class='button-size--medium buttons']//button[@class='btn forward mv-icon-button--primary mv-icon-button--shadow mv-icon-button--medium mv-button mv-icon-button']")

while True:
    try:
        if scroll != None:
            scroll.click()
    except ElementNotInteractableException:
        break

product_all = []

for i in range(0, 16):
    cards_all = {}
    id = i
    name = block_carts.find_elements(By.XPATH, "//div[contains(@class, 'product-mini-card__name')]")[i].text
    price = block_carts.find_elements(By.XPATH, "//div[contains(@class, 'product-mini-card__price')]")[i].text.replace(' ', '').split('\n')[0]
    # Сохраняем в БД
    cards_all['_id'] = id
    cards_all['name'] = name
    cards_all['price'] = price
    collection.insert_one(cards_all)
    # product_all.append(cards_all)

# pprint(product_all)
driver.quit()

