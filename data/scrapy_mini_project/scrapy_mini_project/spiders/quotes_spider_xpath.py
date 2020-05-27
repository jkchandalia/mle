import scrapy

class QuotesSpider(scrapy.Spider):
    name = "xpath-scraper-results"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div/*[@class="quote"]'):
            yield {
                'text':  quote.xpath('//span/text()').get(),
                'author': quote.xpath('//span/small/text()').get(),
                'tags': quote.xpath('//div/*[@class="tags"]/a/text()').getall(),
            }

        next_page = response.xpath('//li/a/@href').get()
        print('next_page', next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)