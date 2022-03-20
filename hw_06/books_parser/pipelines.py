# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

from books_parser.spiders.labirintru import LabirintruSpider
from books_parser.spiders.book24ru import Book24ruSpider

class BooksParserPipeline:
    def __init__(self):
        # Подключаем mongo
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.books
        self.mongo_base[LabirintruSpider.name].drop()
        self.mongo_base[Book24ruSpider.name].drop()

    def process_item(self, item, spider):
        # print()
        # # * Автор(ы)
        # item['author'] = self.unpack(item.get('author'))
        # # id
        # item['_id'] = self.unpack(item.get('_id'))
        # 2 подхода:
        # 1-й collection = self.mongo_base['']
        # 2-й: "spider.name" - обращение к имени паука
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        # print(item)
        return item

    # def unpack(self, element):
    #     """Получаем список на обработку, например: '_id': ['285221'],"""
    #     # tmp = []
    #     # if len(element) == 1:
    #     for el in element:
    #         # print(el)
    #         return el
    

# if __name__ == '__main__':
#     _id = ['285221']
#     BooksParserPipeline.unpack(_id)
#     # BooksParserPipeline.unpack(author)



