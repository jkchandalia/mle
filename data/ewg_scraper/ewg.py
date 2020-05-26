# -*- coding: utf-8 -*-
import scrapy


class EwgSpider(scrapy.Spider):
    name = 'ewg'
    allowed_domains = ['ewg.org']
    start_urls = ['http://www.ewg.org/skindeep/browse/category/Moisturizer_with_SPF/']

    def parse(self, response):
        product_tiles = response.css('div.product-tile')
        for prod in product_tiles:
            item = {
                'name': prod.css('p.product-name::text').extract_first().strip(),
                'company': prod.css('p.product-company::text').extract_first(),
                'score_img_url': prod.css('div.product-score > img::attr(src)').extract_first(), 
                'data_quality': prod.css('div.product-score > p::text').extract_first()
            }
            yield item

        next_page_url = response.css('div.pages > a.next_page::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
