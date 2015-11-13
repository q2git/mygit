# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3,codecs
from os import path

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

#Access========================================================
import pyodbc 
class AccessPipeline(object):
    filename = '../../stock.accdb'
    strConn = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s" %(filename)
    def __init__(self):
        self.conn = None
        dispatcher.connect(self.open_conn, signals.engine_started)
        dispatcher.connect(self.close_conn, signals.engine_stopped)

    def process_item(self, item, spider):
        self.conn.execute('insert into guba values(?,?,?)',tuple(item.values()))
                          #(item['Stock'],item['ID'],item['Date']))
        return item

    def open_conn(self):
        conn = pyodbc.connect(self.strConn)
        conn.autocommit = True
        table = '''create table guba(
            [Stock] text(10),
            [ID] text(50),
            [Date] text(10) 
            )'''
        try:
            conn.execute(table)
        except:
            pass
        #conn.commit()
        self.conn = conn

    def close_conn(self):
        if self.conn is not None:
            #self.conn.commit()
            self.conn.close()
            self.conn = None
        
#sqlite====================================================== 
class SQLiteStorePipeline(object):
    filename = '../../stock.sqlite'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        self.conn.execute('insert into guba values(?,?,?)',
                          (item['Stock'],item['ID'],item['Date']))
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""create table guba
                     (Stock text, ID text,Date datetime)""")
        conn.commit()
        return conn

#text file
import codecs
class BsPipeline(object):
    def __init__(self):
        self.file = codecs.open('../../temp.txt', 'wb','utf_8_sig')
        
    def process_item(self, item, spider):
        #item=''.join(item)
        self.file.write(item['Stock']+','+item['ID']+','+item['Date']+'\r\n')
        #for data in item['Data']:
        #    self.file.write(data+'\r\n')
        return item
    
    def spider_closed(self, spider):
        self.file.close()

#json
import json

class JsonWriterPipeline(object):

   def __init__(self):
       self.file = open('items.txt', 'wb')

   def process_item(self, item, spider):
       line = json.dumps(dict(item)) + "\r\n"
       self.file.write(line)
       return item
     
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        #print type(item)
        if item['title'][0]in self.ids_seen :
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title'][0])
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
        fn = item['Stock']
        if not fn in self.files: # and hasattr(self.files[fn],'write')
            self.files[fn] = codecs.open('../../%s.csv' % fn, 'wb', 'utf_8_sig')
            data = ','.join(item.keys())
            self.files[fn].write(data+'\r\n')

        data = ','.join(item.values())
        self.files[fn].write(data+'\r\n')
        return item    
