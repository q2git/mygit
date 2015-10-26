# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider

from pjs.items import PjsItem


class CsvSpiderSpider(CSVFeedSpider):
    name = 'csv_spider'
    allowed_domains = ['c.com']
    start_urls = ['http://www.c.com/feed.csv']
    # headers = ['id', 'name', 'description', 'image_link']
    # delimiter = '\t'

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        i = PjsItem()
        #i['url'] = row['url']
        #i['name'] = row['name']
        #i['description'] = row['description']
        return i
