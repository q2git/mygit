# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:36:35 2015

@author: 
"""

import urllib2,random
import threading,Queue
from bs4 import BeautifulSoup

HTTP_HEAD = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;Mozilla Firefox 38.2.0 - 10792--72'}
H_HTTP = urllib2.HTTPHandler(0)
H_PROXY=urllib2.ProxyHandler({})
LST = []
CNT = 0
#read proxy list from url and put it into a Queue
class Get_Proxy(threading.Thread):
    def __init__(self,q_url):
        threading.Thread.__init__(self)
        self.q_url = q_url

    def run(self):
        while True:
            url = self.q_url.get()
            html = self.read_html(url)
            self.get_addr(html)
            self.q_url.task_done()
            
    def get_addr(self,html):
        soup=BeautifulSoup(html,'html') 
        mark=soup.find_all('tr',class_=True)
        for addr in mark:
            content=addr.contents[5].string+':'+\
                     addr.contents[7].string+' '+\
                     addr.contents[13].string 
            LST.append(content.lower())# + ' ' + random.choice(['PASS','FAIL','TESTING']))
            #print content,' put into queue.'

    def read_html(self,url):
        req = urllib2.Request(url,None,HTTP_HEAD)
        opener=urllib2.build_opener(H_PROXY,H_HTTP)
        html=''
        try:
            response=opener.open(req)
            html=response.read()
            print 'Done reading from "%s" '%url 
        except urllib2.HTTPError as e:
            print 'Http: ',e
        except urllib2.URLError as e:
            print 'Url: ',e
            
        return html

#write proxy list to a text file
def write_file(prolist,method='wb'):
    try:
        print 'writing proxy address to proxy.txt...'
        f=open('proxy.txt',method)
        for addr in prolist:
            f.write(addr+'\n')
        f.close
        print 'done'
    except Exception as e:
        print 'Excp: ',e

def main():
    
    que_url = Queue.Queue()

    #put URLs to the que_url
    sub=['nn','nt','wn','wt']
    for d in sub:
        for i in range(1,2):
            url = 'http://www.xicidaili.com/%s/%s'%(d,str(i))
            que_url.put(url)

    for x in xrange(5):
        th = Get_Proxy(que_url)
        th.start()   

    
    que_url.join()

    write_file(LST)
    
   
if __name__=='__main__':
    main()
