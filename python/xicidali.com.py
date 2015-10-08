import urllib,urllib2
import os,getpass,threading,time,Queue
from bs4 import BeautifulSoup

HTTP_HEAD = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;Mozilla Firefox 38.2.0 - 10792--72'}
H_HTTP = urllib2.HTTPHandler(0)

#read proxy list from url and put it into a Queue
class Put_proxy(threading.Thread):
    def __init__(self,q_url,q_addr):
        threading.Thread.__init__(self)
        self.q_url = q_url
        self.q_addr = q_addr

    def run(self):
        while True:
            url = self.q_url.get()
            html = self.read_html(url)
            self.get_proxy(html)
            self.q_url.task_done()
            
    def get_proxy(self,html):
        soup=BeautifulSoup(html,'html') 
        mark=soup.find_all('tr',class_=True)
        for addr in mark:
            content=addr.contents[5].string+':'+\
                     addr.contents[7].string+' '+\
                     addr.contents[13].string 
            self.q_addr.put(content.lower())
            #print content,' put into queue.'

    def read_html(self,url):
        req = urllib2.Request(url,None,HTTP_HEAD)
        opener=urllib2.build_opener()
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


#get proxy addr from the Queue and test it
class Test(threading.Thread):
    def __init__(self,q_addr):
        threading.Thread.__init__(self)
        self.q_addr = q_addr
        
    def run(self):
        global cnt
        while True:
            self.test_proxy(self.q_addr.get())
            self.q_addr.task_done()
            time.sleep(0.1)
            cnt=cnt+1

    def test_proxy(self,addr):
        proxy={addr.split(' ')[1]:addr.split(' ')[0]}
        h_proxy=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(h_proxy,H_HTTP)
        try:
            response=opener.open('http://www.google.com',timeout=5).read()
            print '%s-->Testing: %s PASSED'%(self.getName(),proxy)
            lst.append(addr)
            #write_html('%s.html'%cnt,response)
        except Exception as e:
            print '%s-->Testing: %s FAILED'%(self.getName(),proxy)
            #print e
    
#write html
def write_html(fname,html):
    try:
        f=open('/home/carman/Desktop/html/%s'%fname,'w')
        f.write(html)
        f.close
        print 'Done writing html to %s'%fname
    except Exception as e:
        print 'Excp: ',e
        
#write proxy list to a text file
def write_file(prolist,method='wb'):
    try:
        print 'writing proxy address to proxy.txt...'
        f=open('/home/carman/Desktop/proxy.txt',method)
        for addr in prolist:
            f.write(addr+'\r\n')
        f.close
        print 'done'
    except Exception as e:
        print 'Excp: ',e

def main():
    global lst,cnt
    lst = []
    cnt = 0
    t0 = time.time()
    
    que_addr = Queue.Queue()
    que_url = Queue.Queue()

    #put URLs to the que_url
    sub=['nn','nt','wn','wt']
    for d in sub:
        for i in range(1,2):
            url = 'http://www.xicidaili.com/%s/%s'%(d,str(i))
            que_url.put(url)

    th = Put_proxy(que_url,que_addr)
    th.start()
        
    for x in xrange(10):
        th = Test(que_addr)
        th.start()
        time.sleep(0.1)
    
    que_url.join()
    que_addr.join()

    print 'Tested proxy: %d'%cnt
    print 'Elapsed time: %.2fs'%(time.time()-t0)
    write_file(lst)
    
   
if __name__=='__main__':
    main()
