# -*- coding: utf-8 -*-
#import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

class CrSpider(CrawlSpider):
    name = 'cr'
    allowed_domains = ['eastmoney.com']
    #start_urls = ['http://guba.eastmoney.com/news,600596,209423368.html']
    start_urls = map(lambda x:'http://guba.eastmoney.com/list,600596_%d.html'%x,range(1,50))
    rules = (
        #Rule(LinkExtractor(allow=('default_\d+.html'))),
        #Rule(LinkExtractor(allow=('list,600596_\d+\.html',))),
        Rule(LinkExtractor(allow=('news,600596,\d+\.html', )), callback='parse_item'),
    )
    #//div[ngbglistdiv]/ul[@ngblistul2]/li/@href 
    #<a href="topic,600000.html">(600000)浦发银行</a>
            
    def parse_item(self, response):
        #self.logger.info('Hi, this is an item page! %s', response.url)
        #return { 'LINK': response.url} |@id='zwlianame' |@id='zwlitime'
        #{'ID':response.xpath("//div[@id='zwconttbn']//text()").extract(),
        #       'Date':response.xpath("//div[@class='zwfbtime']/text()").extract()}
        for sel in response.xpath("//div[@class='zwli clearfix']|//div[@id='zwconttb']"):
            ID = sel.xpath(".//span[@class='zwnick']//text()|\
            .//div[@id='zwconttbn']//text()").extract_first()
            Date = sel.xpath(".//div[@class='zwlitime']/text()|\
            .//div[@class='zwfbtime']/text()").re_first('\d{4}-\d{2}-\d{2}')
            yield {'ID':ID,'Date':Date}
 
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())   
    process.crawl(CrSpider)
    process.start() # the script will block here until the crawling is finished
