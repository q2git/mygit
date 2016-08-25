# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 19:35:34 2016

@author: PYTHON
"""

# -*- coding: utf-8 -*-
import urllib,urllib2
import threading,time,Queue
from bs4 import BeautifulSoup
import ast
import random

Http_heads = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;Mozilla Firefox 38.2.0 - 10792--72'},
             {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
             {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'},
             {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'},
             {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'},
             {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'},
             {'User-Agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'},
             {'User-Agent': 'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'},
             ]
Http_handler = urllib2.HTTPHandler(debuglevel=0)


class CrawlerProxy(threading.Thread):
    def __init__(self,que_url,lock,proxies):
        threading.Thread.__init__(self)
        self.que_url = que_url
        self.lock = lock
        self.proxies = proxies
        self.start()
        
    def run(self):
        while True:
            proxies = None
            time.sleep(random.randint(5,20))
            url,tds = self.que_url.get()
            filename = 'proxies_all.txt'#.format(url.split('/')[-2])
            html = self._readHtml(url)
            if html is not None:
                proxies = self._fetch_addr(html,tds)
            if proxies is not None:
                with self.lock:
                    with open(filename,'ab') as f:
                        f.writelines(map(lambda s:str(s).lower()+'\r\n',proxies)) 
                    print '-->{0:10}: write {1:4} proxies into {2}'.format(self.getName(),len(proxies),filename)
            self.que_url.task_done()
            if self.que_url.qsize() == 0: break
                    
    def _fetch_addr(self,html,tds):
        proxies = []
        try:
            soup=BeautifulSoup(html,'lxml') 
            mark=soup.find_all('tr')
            for addr in mark[1:]:
                ip = addr.contents[tds[0]].string
                port = addr.contents[tds[1]].string
                http = addr.contents[tds[2]].string
                proxies.append({http:ip+':'+port})           
            return proxies                
        except Exception as e:
            with self.lock:
                print '-->[{0:10} Fetching addr Error: {1:40}] '.format(self.getName(),e)
        
    def _readHtml(self,url):
        run_count = 0
        fail_count= 0
        last_proxy = None
        while 1: #loop until get response
            run_count += 1           
            try:
                if fail_count > 3: #remove proxy which failed >3 times
                    self.proxies.remove(last_proxy) 
                    fail_count = 0 
                if run_count > 30: break #try most 30 times for reading url                 
                proxy = [last_proxy,random.choice(self.proxies)][fail_count==0]
                last_proxy = proxy #store the last proxy
                proxy_handler = urllib2.ProxyHandler(proxy)
                req = urllib2.Request(url,None,random.choice(Http_heads))
                opener = urllib2.build_opener(proxy_handler,Http_handler)                                     
                response = opener.open(req,timeout=10).read()
                return response
            except Exception as e:
                if fail_count > 4: break # error:self.proxies.remove(last_proxy)
                fail_count += 1
                with self.lock:
                    print '-->{0:10}{1:8}{2:<3}{3:35}{4:<5}{5}'.format(
                            self.getName(),url[-6:],run_count,proxy,
                            len(self.proxies),e)      
                time.sleep(5)                         

                
def get_high_anonymous_proxy():
    "return proxy list which read out from text file"
    with open('high_anonymous.txt','r') as f:
        proxies = f.readlines()
    return map(ast.literal_eval, #convert str to dict
                  set(proxies) #remove duplications
                  ) 

def remove_dup_proxies():
    "remove duplications from text file"
    with open('proxies_all.txt','r') as f:
        proxies = f.readlines()
    proxies = map(lambda s:s.lower(), proxies)
    proxies = set(proxies)
    with open('proxies.txt','w') as f:
        f.writelines(proxies)
                  
def make_urls(begin_page,end_page):
    "make Urls for crawler"
    websites = [('http://www.mimiip.com',['gngao','gnpu','gntou','hw'],
                    (1,3,9)),
                ('http://www.xicidaili.com',['nn','nt','wn','wt'],
                    (3,5,11)),
                ]
    for website,subdirs,tds in websites:
        for subdir in subdirs:
            for i in range(begin_page,end_page):
                yield ('{0}/{1}/{2}'.format(website,subdir,i),tds)
                
def main():
    proxies = get_high_anonymous_proxy()
    lock = threading.Lock()  
    que_url = Queue.Queue()
    map(que_url.put, make_urls(1,500))
    
    threads = []
    for th in xrange(20):
        threads.append(CrawlerProxy(que_url, lock, proxies))
    
    #for th in threads:
    #    th.join()
    que_url.join()
    
    with open('proxies_verified.txt','ab') as f:
                    f.writelines(map(lambda s:str(s).lower()+'\r\n',proxies))
    print 'All task done!'
    
   
if __name__=='__main__':  
    main()
    remove_dup_proxies()
