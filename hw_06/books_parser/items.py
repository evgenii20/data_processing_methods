# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # * Наименование книги
    name = scrapy.Field()
    # * Автор(ы)
    author = scrapy.Field()
    # * Основая цена
    basic_price = scrapy.Field()
    # * Цена со скидкой
    discount_price = scrapy.Field()
    # * Рейтинг книги
    rating = scrapy.Field()
    # * Ссылка на книгу
    link = scrapy.Field()
    # * id
    _id = scrapy.Field()
