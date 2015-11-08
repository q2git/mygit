# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class AllSpider(scrapy.Spider):
    name = 'all'
    allowed_domains = ['eastmoney.com']
    stkids = map(lambda x:x.strip(),open('sz.txt','rb').readlines())
    start_urls = ['http://guba.eastmoney.com/list,600596.html']
    #start_urls = map(lambda x:'http://guba.eastmoney.com/list,%s.html'%x,stkids)

    def parse(self,response):
        articles = response.xpath("//div[@class='pager']/text()").re_first('\d+')
        #print articles,int(articles)/80
        stock = response.url.split(',')[1].split('.')[0]
        
 
if __name__ == '__main__':    
    process = CrawlerProcess(get_project_settings())   
    process.crawl(AllSpider)
    process.start() # the script will block here until the crawling is finished
