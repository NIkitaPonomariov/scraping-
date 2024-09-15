import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_text = quote.css('span.text::text').get()
            author_name = quote.css('span small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()

            # Скрапимо деталі автора (перехід на сторінку автора)
            author_page_link = quote.css('span a::attr(href)').get()
            author_page_link = response.urljoin(author_page_link)

            # Зберігаємо цитати
            yield {
                'quote': quote_text,
                'author': author_name,
                'tags': tags
            }

            # Викликаємо метод парсингу автора
            yield scrapy.Request(author_page_link, callback=self.parse_author)

        # Переходимо на наступну сторінку
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_author(self, response):
        author_name = response.css('h3.author-title::text').get().strip()
        birth_date = response.css('span.author-born-date::text').get()
        birth_place = response.css('span.author-born-location::text').get().strip("in ")
        description = response.css('div.author-description::text').get().strip()

        # Зберігаємо інформацію про автора
        yield {
            'author': author_name,
            'birth_date': birth_date,
            'birth_place': birth_place,
            'description': description
        }

# Запуск через Python
process = CrawlerProcess(settings={
    'FEEDS': {
        'quotes.json': {'format': 'json'},
        'authors.json': {'format': 'json'}
    }
})

process.crawl(QuotesSpider)
process.start()
