# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PjsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SapItem(scrapy.Item):
    SAPPart = scrapy.Field()
    Desc = scrapy.Field()
    
