# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

class CrSpider(CrawlSpider):
    name = 'cr'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://guba.eastmoney.com/list,600596.html']

    rules = (
        Rule(LinkExtractor(allow=('600596_2.html'))),
        #Rule(LinkExtractor(allow=('default_\d+.html'))),
        #Rule(LinkExtractor(allow=('list,600596_\d+\.html',))),
        Rule(LinkExtractor(allow=('news,600596,\d{9}\.html', )), callback='parse_item'),
    )
    #//div[ngbglistdiv]/ul[@ngblistul2]/li/@href 
    #<a href="topic,600000.html">(600000)浦发银行</a>
    def parse_item(self, response):
        #self.logger.info('Hi, this is an item page! %s', response.url)
        return { 'LINK': response.url}

 
if __name__ == '__main__':

    #process = CrawlerProcess({
    #        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    #    }) 
    process = CrawlerProcess(get_project_settings())   
    process.crawl(CrSpider)
    process.start() # the script will block here until the crawling is finished
