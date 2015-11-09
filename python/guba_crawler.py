# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from multiprocessing import Process,Queue,Pool,Manager
import time,re,codecs,os
import pyodbc 

#######################################
def WriteAccess(q_items):
    filename = 'stock.accdb'
    strConn = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s" %(filename)
    conn = pyodbc.connect(strConn)
    conn.autocommit = True
    table = '''create table guba([Stock] text(20),[Price] text(20),
    [People] text(20),[Article] text(20),[Date] text(20))'''
    try:
        conn.execute(table)
    except:
        pass
    while 1:
        item = q_items.get()
        if item == None:break
        conn.execute('insert into guba values(?,?,?,?,?)',item)
    conn.close()
    conn = None

def WriteTxt(q_items):
    with codecs.open('gubaitems.txt','wb','utf_8_sig') as f:
        while 1:
            item = q_items.get()
            if item == None:break
            print 'writtig [%s] to gubaitems.txt'%item
            f.write(item)
        
#######################################
def GetGubaItems(driver,q_urls,q_items):
    print 'Proceess id: %s'%os.getpid()
    while 1:
        url = q_urls.get()
        if url == None:q_urls.put(None);break
        print 'fetching data from %s'%url
        '''
        driver.get(url)
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html) 
        stock = soup.find('span',attrs={'id':'stockheadercode'}).get_text()[1:7]
        price = soup.find('span',attrs={'id':'hqprice'}).get_text()
        people = re.match('\d+',soup.find('span',attrs={'id':'stockifm'}).get_text()).group()
        article = soup.find('div',attrs={'class':'pager'}).get_text().split(' ')[1]
        date =  time.strftime("%Y-%m-%d",time.localtime(time.time()))
        q_items.put((stock,price,people,article,date))
        '''
        q_items.put(url)

#######################################
def main():
    manager = Manager()
    q_urls = manager.Queue()
    q_items =manager.Queue()
    #put urls into q_urls
    urls = map(lambda x:'http://guba.eastmoney.com/list,600596_%s.html'%x,range(1,10))
    for url in urls:
        print 'putting url %s'%url
        q_urls.put(url)
    
    #get guba items and put it into q_items
    driver = ''#webdriver.Firefox()
    pool = Pool()
    
    pool.apply_async(GetGubaItems, args=(driver,q_urls,q_items))
    
    #write guba items to access database
    #dbwrite = Process(target=WriteAccess, args=(q_items,))
    #dbwrite = Process(target=WriteTxt, args=(q_items,))
    #dbwrite.start()
    
    #block here until all subprocesses done
    pool.close()
    pool.join()
    q_items.put(None)    
    #dbwrite.join()
    
    #driver.close()
    print 'all tasks done'
    
if __name__ == '__main__':
    main()
