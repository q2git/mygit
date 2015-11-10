# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import threading, Queue
import time,re,codecs,os
import pyodbc 

#######################################
def WriteAccess(q_items):
    filename = unicode(os.path.abspath('stock.accdb'),'gbk')#utf8
    strConn = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s" %(filename)
    conn = pyodbc.connect(strConn)
    conn.autocommit = True
    table = '''create table guba([Stock] varchar(20),[Price] float,
    [People] int,[Article] int,[Date] datetime)'''
    try:
        conn.execute(table)
    except:
        pass
    while 1:
        item = q_items.get()
        if item == None:break
        print 'DBW:%s...'%str(item),
        try:
            conn.execute('insert into guba values(?,?,?,?,?)',item)
            print 'Done.'
        except:
            print 'FAIL.'
    conn.close()
    conn = None

def WriteTxt(q_items):
    with codecs.open('gubaitems.txt','wb','utf_8_sig') as f:
        while 1:
            item = q_items.get()
            if item == None:break
            print 'writtig %s'%str(item)
            f.write(str(item)+'\r\n')
        
#######################################
def GetGubaItems(q_urls,q_items,lock):
    driver = webdriver.PhantomJS()
    while 1:
        url = q_urls.get(timeout=3)
        if url == None:q_urls.put(None);break
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml') 
        stock = soup.find('span',attrs={'id':'stockheadercode'}).get_text()[1:7]
        price = soup.find('span',attrs={'id':'hqprice'}).get_text()
        people = re.match('\d+',soup.find('span',attrs={'id':'stockifm'}).get_text()).group()
        article = soup.find('div',attrs={'class':'pager'}).get_text().split(' ')[1]
        date =  time.strftime("%Y-%m-%d",time.localtime(time.time()))
        data = (stock,price,people,article,date)
        q_items.put(data)
        with lock:
            print 'PID%s:%s %s left'%(os.getpid(),data,q_urls.qsize())
    driver.close()
    
def Urls2Que(q_urls):
    print 'Putting urls into [q_urls]...',
    stkids = map(lambda x:x.strip(),open('sz.txt','rb').readlines())
    urls = map(lambda x:'http://guba.eastmoney.com/list,%s.html'%x,stkids)
    map(q_urls.put,urls)
    q_urls.put(None)
    print ' Done.'
    
#######################################
def main():
    q_urls = Queue.Queue()
    q_items = Queue.Queue()
    lock = threading.Lock()
    #put urls into q_urls
    Urls2Que(q_urls)
    
    #get guba items and put it into q_items
    th_num = raw_input('Please set the number of threads:')
    th_num = int(th_num) if th_num.isdigit() else 5
    ths = []
    for x in range(th_num):
        th = threading.Thread(target=GetGubaItems, args=(q_urls,q_items,lock))
        th.start()
        ths.append(th)
    for th in ths:
        th.join()
    q_items.put(None)

    #write guba items to access database
    WriteAccess(q_items)
    #WriteTxt(q_items)

    print 'all tasks done'
    
if __name__ == '__main__':
    main()
