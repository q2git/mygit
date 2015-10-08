import urllib,urllib2
import os,getpass,threading,time,Queue
from bs4 import BeautifulSoup

HTTP_HEAD = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;Mozilla Firefox 38.2.0 - 10792--72'}
proxy = {}
H_PROXY = urllib2.ProxyHandler(proxy)
H_HTTP = urllib2.HTTPHandler(0)

#read proxy list from url and put it into a Queue
class Put_proxy(threading.Thread):
    def __init__(self,q_url,q_addr):
        threading.Thread.__init__(self)
        self.q_url = q_url
        self.q_addr = q_addr

    def run(self):
        html = self.read_html(self.q_url.get())
        soup=BeautifulSoup(html,'html') 
        mark=soup.find_all('tr',class_=True)
        for addr in mark:
            content=addr.contents[5].string+':'+\
                     addr.contents[7].string+' '+\
                     addr.contents[13].string 
            self.q_addr.put(content)
            print content,' put into queue.'

    def read_html(self,url):
        req = urllib2.Request(url,None,HTTP_HEAD)
        opener=urllib2.build_opener(H_PROXY)
        html=''
        try:
            print 'reading web content from "%s" ...'%url
            response=opener.open(req)
            html=response.read()
            print 'done.'
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
        addr = self.q_addr.get(0)
        proxy={addr.split(' ')[1]:addr.split(' ')[0]}
        h_proxy=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(h_proxy,H_HTTP)
        try:
            print '%s -->Testing proxy: %s ...'%(self.getName(),proxy)
            #response=opener.open('http://www.google.com',timeout=1)
            #print 'PASS.'
            lst.append(addr)
        except Exception as e:
            print 'FAIL.'
            print e

    

#write proxy list to a text file
def write_file(prolist,method='wb'):
    try:
        print 'writing proxy address to proxy.txt...'
        f=open('proxy.txt',method)
        cnt=1
        for addr in prolist:
            f.write(addr+'\r\n')
            cnt+=1
        f.close
        print 'done'
    except Exception as e:
        print 'Excp: ',e

def main():
    global lst
    lst=[]
    que_addr = Queue.Queue()
    que_url = Queue.Queue()

    #put URLs to the que_url
    sub=['nn']#,'nt','wn','wt']
    for d in sub:
        for i in range(1,3):
            url = 'http://www.xicidaili.com/%s/%s'%(d,str(i))
            print url
            que_url.put(url)


    while not que_url.empty():
        th = Put_proxy(que_url,que_addr)
        th.start()
        time.sleep(0.3)
        
        th = Test(que_addr)
        th.start()
        time.sleep(0.3)

        while True:
            if (len(threading.enumerate()) < 5):
                break
            
    write_file(lst)
'''

if __name__=='__main__':
    main()
