# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

class CrSpider(CrawlSpider):
    name = 'cr'
    allowed_domains = ['eastmoney.com']
    start_urls = []
    #start_urls = ['http://guba.eastmoney.com/list,600596.html']
    #start_urls = map(lambda x:'http://guba.eastmoney.com/list,%s.html'%x.strip(),open('sz.txt','rb').readlines())
    #start_urls = map(lambda x:'http://guba.eastmoney.com/list,002425_%d.html'%x,range(1,2))
    rules = (
        #Rule(LinkExtractor(allow=('list,\d{6}\.html')),callback='get_pages'),
        #Rule(LinkExtractor(allow=('list,\d{6}\.html',))),
        Rule(LinkExtractor(allow=('news,\d{6},\d+\.html', )), callback='parse_item'),
    )
    
    def __init__(self, *args, **kwargs):
        super(CrSpider, self).__init__(*args, **kwargs)
        urls = map(lambda x:'http://guba.eastmoney.com/list,%s_'%x.strip(),open('sz.txt','rb').readlines())
        for x in urls:
            for y in range(1,10):
                self.start_urls.append(x+str(y)+'.html')
            
    def get_pages(self,response):
        articles = response.xpath("//div[@class='pager']/text()").re_first('\d+')
        print articles,int(articles)/80

        
    def parse_item(self, response):
        x = GubaItem()
        x['Stock'] = response.url.split(',')[1]
        #return { 'LINK': response.url} |@id='zwlianame' |@id='zwlitime'
        #{'ID':response.xpath("//div[@id='zwconttbn']//text()").extract(),
        #       'Date':response.xpath("//div[@class='zwfbtime']/text()").extract()}
        for sel in response.xpath("//div[@class='zwli clearfix']|//div[@id='zwconttb']"):
            x['ID'] = sel.xpath(".//span[@class='zwnick']//text()|\
            .//div[@id='zwconttbn']//text()").extract_first()
            x['Date'] = sel.xpath(".//div[@class='zwlitime']/text()|\
            .//div[@class='zwfbtime']/text()").re_first('\d{4}-\d{2}-\d{2}')
            yield x #{'Stock':Stock,'ID':ID,'Date':Date}

 
if __name__ == '__main__':
        #for fixing import error    
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from items import GubaItem
    else:
        from guba.items import GubaItem
        
    process = CrawlerProcess(get_project_settings())   
    process.crawl(CrSpider)
    process.start() # the script will block here until the crawling is finished
