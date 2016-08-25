# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 20:17:39 2016

@author: PYTHON
"""

#!/usr/bin/python  
#coding=utf-8  
  
import urllib  
import urllib2  
import time
import Queue
import threading
import ast
    
user_agent='Mozilla/5.0 (Windows NT 6.1; \
WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;\
Mozilla Firefox 38.2.0 - 10792--72'
headers={'User-Agent':user_agent}
'''  
def post(url, data): 
    req = urllib2.Request(url,None,headers)  
    data = urllib.urlencode(data)  
    #enable cookie  
    opener = urllib2.build_opener(proxy_handler)  
    response = opener.open(req, data,timeout=3)  
    return response.read()  
'''  
def vote(th,que,lock):
    posturl = "http://gtxxswx.gzrailway.com.cn/vote/tj"  
    data = {'ids':'53', 'type':2+1} 
    data = urllib.urlencode(data) 
    while 1:
        proxy = que.get()
        if proxy == None or que.empty():que.put(None);break 
        proxy_handler=urllib2.ProxyHandler(proxy)
        req = urllib2.Request('http://hq.sinajs.cn/list=sh600367',None,headers)
        #req = urllib2.Request(posturl,None,headers)   
        opener = urllib2.build_opener(proxy_handler) 
        try:
            rsp = opener.open(req, data,timeout=5)
            rsp = rsp.read()
            with lock:     
                print que.qsize(),th,rsp

        except Exception as e:
            with lock:     
                print que.qsize(),th,'--',e
        
    #time.sleep(2)

def main():
    que_proxy = Queue.Queue()
    lock = threading.Lock() 
    prox = open('proxies.txt','r').readlines()
    prox = [pro for pro in prox]
    prox = set(prox) #remove duplications
    prox = map(ast.literal_eval, prox) #convert to dict list
    map(que_proxy.put,prox)
    que_proxy.put(None)
    #print prox
    ths =[]
    for x in xrange(10):
        name = 'TH-{}:'.format(x)
        th = threading.Thread(target=vote, args=(name,que_proxy,lock))
        th.start()
        ths.append(th)
    for th in ths:
        th.join()
        
    #que_proxy.join()
    print 'All done'
            
if __name__ == '__main__':  
    main()  