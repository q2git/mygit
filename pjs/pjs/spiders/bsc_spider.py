# -*- coding: utf-8 -*-
import scrapy


class BscSpiderSpider(scrapy.Spider):
    name = "bsc_spider"
    allowed_domains = ["b.com"]
    start_urls = (
        'http://www.b.com/',
    )

    def parse(self, response):
        pass
