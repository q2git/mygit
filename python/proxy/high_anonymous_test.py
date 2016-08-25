# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 18:20:57 2016

@author: PYTHON
"""

# -*- coding: utf-8 -*-
import urllib,urllib2
import threading,Queue
import ast

Http_handler = urllib2.HTTPHandler(debuglevel=0)

class ProxyTest(threading.Thread):
    def __init__(self,que_proxy,lock,test_url):
        threading.Thread.__init__(self)
        self.url = test_url
        self.lock = lock
        self.que_proxy = que_proxy
        self.start()
        
    def run(self):
        if self._checkme_if_blocked():
            while 1:
                proxy = self.que_proxy.get()
                if self._test_proxy(proxy):
                    self._write_txt(proxy)
                self.que_proxy.task_done()
                if self.que_proxy.qsize() == 0:break
        else:
            print 'You have not been blocked.'

    def _checkme_if_blocked(self): 
        "check my ip whether it was blocked or not"
        try:
            urllib2.urlopen(self.url).read()
        except urllib2.HTTPError as e:
            if e.code == 503: return True 
        except:                                             
            return False 
                           
    def _test_proxy(self,proxy):
        "test the proxy if it has blocked by target website"
        count = 0
        while count < 3:
            count += 1 
            try:
                proxy_handler = urllib2.ProxyHandler(proxy)
                req = urllib2.Request(self.url)
                opener = urllib2.build_opener(proxy_handler,Http_handler)                                     
                opener.open(req,timeout=10).read(10)
                count = 0
                return True
            except urllib2.HTTPError as e:
                if e.code == 503: return False
            except:
                return False
            finally:
                with self.lock:
                    print '-->{0:10},{1:40},left:{2:6}, {3}'.format(
                    self.getName(),proxy,self.que_proxy.qsize(),
                    ['FAIL','PASS'][count==0])                

    def _write_txt(self,proxy):
        "write passed proxy into text file"
        with self.lock:
            with open('high_anonymous.txt','ab') as f:
                f.write(str(proxy)+'\r\n')
            print '-->{0} is a high anonymous proxy'.format(proxy)
            
               
def read_proxies():
    "return proxy list which read out from text file"
    with open('proxies.txt','r') as f:
        proxies = f.readlines()
    return map( ast.literal_eval, #convert str to dict
                set(proxies) #remove duplications
                ) 
              
def main():
    test_url = 'http://www.mimiip.com/gngao/1'
    #test_url = 'http://www.xicidaili.com/nn/1'
    proxies = read_proxies()
    lock = threading.Lock()  
    que_proxy = Queue.Queue()
    map(que_proxy.put, proxies) #put proxies into queue
    
    threads = []
    for th in xrange(50):
        threads.append(ProxyTest(que_proxy, lock, test_url))
    
    for th in threads:
        th.join()
        
    #que_proxy.join() 
    print "All task done."
    
if __name__=='__main__':  
    #print read_proxies()[3]
    main()
