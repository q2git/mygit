from scrapy import signals
from scrapy.exporters import XmlItemExporter

class XmlExportPipeline(object):
    def __init__(self):
        self.files = {}
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s.xml' % spider.name, 'wb')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

##########################################
class TxtPipeline(object):
    def __init__(self):
        self.files = {}
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass
        #file = open('%s.txt' % spider.name, 'wb')
        #self.files[spider] = file
    
    def spider_closed(self, spider):
        for i in self.files:
            file = self.files.pop(i)
            file.close()

    def process_item(self, item, spider):
        fn = item['filename']
        if not fn in self.files: # and hasattr(self.files[fn],'write')
            self.files[fn] = open('%s.txt' % fn, 'wb')

        data = ','.join(item.values())
        self.files[fn].write(data+'\r\n')
        return item
