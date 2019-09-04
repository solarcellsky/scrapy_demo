# -*- coding: utf-8 -*-
import scrapy
from maoyanhot.items import MaoyanhotItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/7']

    def parse(self, response):
        dl = response.css('.board-wrapper dd')
        for dd in dl:
            item = MaoyanhotItem()
            item['index'] = dd.css('.board-index::text').extract_first()
            item['title'] = dd.css('.name a::text').extract_first()
            item['star'] = dd.css('.star::text').extract_first()
            item['releasetime'] = dd.css('.releasetime::text').extract_first()
            item['score'] = dd.css('.score .integer::text').extract_first() + '' + dd.css('.score .fraction::text').extract_first()
            yield item
        pass
