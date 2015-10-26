# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider

from pjs.items import PjsItem


class XmlSpiderSpider(XMLFeedSpider):
    name = 'xml_spider'
    allowed_domains = ['c.com']
    start_urls = ['http://www.c.com/feed.xml']
    iterator = 'iternodes' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        i = PjsItem()
        #i['url'] = selector.select('url').extract()
        #i['name'] = selector.select('name').extract()
        #i['description'] = selector.select('description').extract()
        return i
