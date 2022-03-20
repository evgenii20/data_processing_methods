import re
import scrapy
from scrapy.http import HtmlResponse

from books_parser.items import BooksParserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    text_search = 'Информационные технологии'
    page_number = 1
    url = 'https://www.labirint.ru'
    start_urls = [f'{url}/search/{text_search}']
    #links = []

    # # def link_join(self, response: HtmlResponse):
    # def link_join(self, response: HtmlResponse):
    #     urls_list = response.xpath("//a[@class='product-title-link']/@href").getall()
    #     tmp_list = []
    #     for link in urls_list:
    #         tmp_list.append(self.url + link)
    #
    #     return tmp_list

    def parse(self, response: HtmlResponse):
        """Метод обрабатывает пагинацию и делает сбор ссылок для
        перехода на целевую страницу"""
        # получаем ссылку на следующую страницу. get() - вернёт одно значение "page" из списка, на следующую страницу
        # 1-е действие
        print()
        
		next_page = response.xpath("//div[@class='pagination-next']/a/@href").get()

        if next_page:
            # возврат callback
            yield response.follow(next_page, callback=self.parse)

        # 2-е действие
        # получаем все значения getall
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        # 3-е действие
        # for link in self.links:
        for link in links:
            # item = {}
            print()
            # follow инициализирует передачу response на url "link" в callback" и
            # одновременно с этим дергает метод "parse" в котором он был вызван
            # Переходим по ссылке: '/books/811299/' и парсим текст на странице
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        """Метод выполняет парсинг данных после перехода на страницу источника"""
        print('response.url: ', response.url)
        # print()
        # name = response.xpath("//span[@class='product-title']/text()").get()
		# Наименование книги
        name = response.xpath("//h1/text()").get()
        # # * Автор(ы)
        author = response.xpath("//div[contains(text(), 'Автор: ') and contains(@class, 'authors')]/a/text()").getall()
        # # * Основая цена
        basic_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        # # * Цена со скидкой
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        # # * Рейтинг книги
        rating = response.xpath("//div[@id='rate']/text()").get()
        # # * Ссылка на книгу, например: 'https://www.labirint.ru/books/811299/'
        link = response.url
        # # * id
        # regex = f'r"(\d{0,10}[0-9])"'
        _id = re.findall(r'(\d{0,10}[0-9])', link)[-1]
        
		yield BooksParserItem(
            name=name,
            author=author,
            basic_price=basic_price,
            discount_price=discount_price,
            rating=rating,
            link=link,
            _id=_id,
        )
