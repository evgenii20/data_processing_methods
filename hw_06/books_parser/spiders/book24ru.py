import re

import scrapy
from scrapy.http import HtmlResponse
from books_parser.items import BooksParserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    # start_urls = ['http://book24.ru/']
    # Пример запроса: "https://book24.ru/search/?q=новинки"
    text_search = 'новинки'
    url = 'https://book24.ru'
    start_urls = [f'{url}/search/?q={text_search}']
    # Пример с разбивкой на страницы:
    # https://book24.ru/search/page-2

    def parse(self, response):
        """Метод обрабатывает пагинацию и делает сбор ссылок для
                перехода на целевую страницу"""
        # получаем ссылку на следующую страницу. get() - вернёт одно значение "page" из списка, на следующую страницу
        # 1-е действие
        print('response.url:\n', response.url)
        # print()
        # Получаем номер следующей страницы:
        if response.status == 200:
            # next_page = response.xpath("//li[@class='pagination__button-item _next']/a/@href").get()
			# Получаем блок с количеством карточек в запросе
            card = response.xpath("//div[@class='search-page__desc']").get()
			# Получаем цифровое значение
            cards = re.findall(r'(\d{0,10}[0-9])', card)
            # округляем (round) в большую сторону
            pages = round(int(self.unpack(cards))/30)

            for page in range(1, pages+1):
				# создаём ссылку на страницу карточек:
                next_page = f'/page-{page}/'
                # if 'page-' in response.url:
                # #     response_ = response.url.replace(f'?page={self.page_number}', '')
                #     next_page = f'page-{page}' + response.xpath("//div/a[@class='pagination-next__text']/@href").get()
                # #     self.page_number += 1
                # #     # "pagination-next__text disabled"
                # # else:
                # #     next_page = f'{response.url}?page={self.page_number}'

                if next_page:
                    # возврат callback
                    yield response.follow(next_page, callback=self.parse)

                # 2-е действие
                # получаем все значения getall
                links = response.xpath("//a[@class='product-card__name smartLink']/@href").getall()
                # 3-е действие
				# пример ссылок:
                # 00 = {str} '/product/aspid-5911547/'
                # 01 = {str} '/product/na-volnakh-origami-muzykalnyy-privorot-5993423/'
                for link in links:
                    # print()
                    # follow инициализирует передачу response на url "link" в callback" и
                    # одновременно с этим дёргает метод "parse" в котором он был вызван
                    # Переходим по ссылке: '/books/811299/' и парсим текст на странице
                    yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        """Метод выполняет парсинг данных после перехода на страницу источника"""
        # print('response.url: ', response.url)
        # print()
        # name = response.xpath("//span[@class='product-title']/text()").get()

        name = response.xpath("//h1/text()").get().strip()
        # # * Автор(ы)
        author = response.xpath("//a[@class='product-characteristic-link smartLink' and "
                                "contains(@href, '/author/')]/text()").getall()
        # # * Основая цена  ' 515 ₽ '
        try:
            basic_price = response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").get().replace(' ₽','').strip()
        except AttributeError:
            #     print(f'Нет аттрибута для замены: {basic_price}')
            basic_price = None
        # # * Цена со скидкой   ' 469 ₽ '
        discount_price = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").get()\
            .replace(' ₽','').strip()
        # # * Рейтинг книги ' 4,8 '
        rating = response.xpath("//span[@class='rating-widget__main-text']/text()").get().strip()
        # # * Ссылка на книгу, например: 'https://www.labirint.ru/books/811299/'
        link = response.url
        # # id  ['24', '5993423']
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

    def unpack(self, element):
        """Получаем список на обработку, например: '_id': ['285221'],"""
        # tmp = []
        # if len(element) == 1:
        for el in element:
            # print(el)
            return el

# if __name__ == '__main__':
#     text_search = 'новинки'
#     # page_number = 1
#     # start_urls = [f'https://www.labirint.ru/search/{text_search}/?stype=0']
#     url = 'https://book24.ru'
#     start_urls = [f'{url}/search/?q={text_search}']
#     book = Book24ruSpider()
#     book.parse(start_urls)
