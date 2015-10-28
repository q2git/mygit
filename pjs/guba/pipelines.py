# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from os import path

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class SQLiteStorePipeline(object):
    filename = 'data.db'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        self.conn.execute('insert into TGB values(?,?,?)',
                          (''.join(item['link']),''.join(item['title']),''.join(item['content'])))
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
        conn.execute("""create table TGB
                     (url text, title text,content text)""")
        conn.commit()
        return conn
        
        
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BsPipeline(object):
    def __init__(self):
       self.file = open('temp.txt', 'wb')
       
    def process_item(self, item, spider):
        self.file.write(str(item)+'\r\n')
        return item
        


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
 
     
