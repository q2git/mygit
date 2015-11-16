# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


class CrSpider(CrawlSpider):
    name = 'one'
    allowed_domains = ['eastmoney.com']
    #start_urls = ['http://guba.eastmoney.com/list,'+stkid+'.html']
    #def pvalue(value):
        #print value
        #return value
    def __init__(self, stkpgs, *args, **kwargs):
        super(CrSpider, self).__init__(*args, **kwargs)
        self.stkid,self.pages = stkpgs
        self.start_urls = map(lambda x:'http://guba.eastmoney.com/list,%s_%d.html'
                         %(self.stkid,x),range(1,self.pages))
        self.rules = (
        #Rule(LinkExtractor(allow=('list,'+stkid+'\.html')),callback='get_pages'),
        #Rule(LinkExtractor(allow=('list,'+stkid+'_\d+\.html'),
        #     restrict_xpaths=("//div[@class='articleh' and span[6][starts-with(.,'11-11')]]/span[3]"),
        #     process_value=pvalue)),                        
        Rule(LinkExtractor(allow=('news,'+self.stkid+',\d+\.html', )), callback='parse_item'),
        )

    def get_pages(self,response):
        articles = response.xpath("//div[@class='pager']/text()").re_first('\d+')
        for i in range(2,int(articles)/80):
            url = response.urljoin('list,%s_%s.html'%(self.stkid,i))
            yield scrapy.Request(url)
      
    def parse_item(self, response):
        x = GubaItem()
        x['Stock'] = response.url.split(',')[1]
        for sel in response.xpath("//div[@class='zwli clearfix']|//div[@id='zwconttb']"):
            x['ID'] = sel.xpath(".//span[@class='zwnick']//text()|\
            .//div[@id='zwconttbn']//text()").extract_first()
            x['Date'] = sel.xpath(".//div[@class='zwlitime']/text()|\
            .//div[@class='zwfbtime']/text()").re_first('\d{4}-\d{2}-\d{2}')
            yield x

     
        
if __name__ == '__main__':
        #for fixing import error    
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from items import GubaItem
    else:
        from guba.items import GubaItem
    stkid = raw_input('please input the stock id:')
    pages = int(raw_input('please input the total pages:'))
        
    process = CrawlerProcess(get_project_settings())   
    process.crawl(CrSpider,(stkid,pages))
    process.start() # the script will block here until the crawling is finished
