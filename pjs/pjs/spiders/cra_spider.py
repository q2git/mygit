# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

class CrSpider(CrawlSpider):
    name = 'cr'
    #allowed_domains = ['example.com']
    start_urls = ['file:///D:/02_BOMs/test.HTM']

    rules = (
        Rule(LinkExtractor(allow=('Index.htm'))),
        Rule(LinkExtractor(allow=('.HTM', )), callback='parse_item'),
    )
    
    def parse_item(self, response):
        #self.logger.info('Hi, this is an item page! %s', response.url)
        #print response.url
        return {'SAPPart':response.xpath('//nobr[@id="l0003022"]/text()').extract_first(),
               'Desc' :response.xpath('//nobr[@id="l0004022"]/text()').extract_first()
               }


 
if __name__ == '__main__':

    #process = CrawlerProcess({
    #        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    #    }) 
    process = CrawlerProcess(get_project_settings())   
    process.crawl(CrSpider)
    process.start() # the script will block here until the crawling is finished
