# -*- coding: utf-8 -*-
import codecs
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

#from pjs.items import SapItem

class BsSpider(scrapy.Spider):
    name = "bs"
    allowed_domains = ['eastmoney.com']

    start_urls = [
    #    "file:///D:/02_BOMs/BACKUP/Index.htm",
        "http://guba.eastmoney.com/news,600596,189798600.html",
    ]
    '''
    def __init__(self, PN=[], *args, **kwargs):
            super(BsSpider, self).__init__(*args, **kwargs)
            for item in PN:
                self.start_urls.append('file:///D:/02_BOMs/%s' % item)
    '''
        
    def parse(self,response):
        with codecs.open('tmp.html','wb','utf_8_sig') as f:
            f.write(response.body)
        '''
        l = ItemLoader(item=SapItem(), response=response)
        l.add_xpath('SAPPart','//nobr[@id="l0003022"]/text()')
        l.add_xpath('Desc','//nobr[@id="l0004022"]/text()')
        #l.default_input_processor = MapCompose()
        l.default_output_processor = Join()
        return l.load_item()
        #return {'SAPPart':response.xpath('//nobr[@id="l0003022"]/text()').extract(),
        #       'Desc' :response.xpath('//nobr[@id="l0004022"]/text()').extract()
        #       }
        #for href in response.xpath('//a[@class="file"]/@href').extract():
        #    url = href#response.urljoin(href)
            #yield scrapy.Request(url, callback=self.parse_bom,dont_filter=True)
    
    def parse_bom(self, response):
        #for item in response.xpath('//nobr'):
        print response.url
        return {'SAPPart':response.xpath('//nobr[@id="l0003022"]/text()').extract(),
               'Desc' :response.xpath('//nobr[@id="l0004022"]/text()').extract()
               }

    '''
 
    ''' 
    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):

        for sel in response.xpath('//ul/li'):

            yield {'title': sel.xpath('a/text()').extract()}#,
                   #'link': sel.xpath('a/@href').extract(),
                   #'desc': sel.xpath('text()').extract()}

    '''      
    '''
    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
    '''
  
if __name__ == '__main__':
    #for fixing import error    
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from items import SapItem
    else:
        from guba.items import SapItem
    '''    
    import os
    l = os.listdir(r'D:\02_BOMs')
    lf = []
    for f in l:
        if f[-3:] == 'HTM':
            lf.append(f)
    '''
    #process = CrawlerProcess({
    #        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    #    }) 
    process = CrawlerProcess(get_project_settings())   
    process.crawl(BsSpider)
    process.start() # the script will block here until the crawling is finished

