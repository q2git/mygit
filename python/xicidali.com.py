#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import urllib,urllib2
import os
from bs4 import BeautifulSoup

#test proxy
def test_proxy(prolist):
    tested_proxy=[]
    h_http = urllib2.HTTPHandler(0)
    for item in prolist:
        proxy={item.split(' ')[1]:item.split(' ')[0]}
        h_proxy=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(h_proxy,h_http)
        try:
            print 'Testing proxy: %s ...'%proxy,
            response=opener.open('http://www.google.com',timeout=1)
            print 'PASS.'
            tested_proxy.append(item)
        except Exception as e:
            print 'FAIL.'
            print e
            
    return tested_proxy

    
#read html
def read_html(url):
    user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;Mozilla Firefox 38.2.0 - 10792--72'
    header={'User-Agent':user_agent}
    req = urllib2.Request(url,None,header)
    html=''
    try:
        print 'reading web content from "%s" ...'%url
        response=urllib2.urlopen(req)
        html=response.read()
        print 'done.'
    except urllib2.HTTPError as e:
        print 'Http: ',e
    except urllib2.URLError as e:
        print 'Url: ',e

    return html

def get_prolist(html):
    prolist=[]
    soup=BeautifulSoup(html,'lxml') 
    mark=soup.find_all('tr',class_=True)
    for addr in mark:
        content=addr.contents[5].string+':'+\
                 addr.contents[7].string+' '+\
                 addr.contents[13].string 
        prolist.append(content.lower())
    #print str(prolist)
    return prolist

def write_file(prolist,method='wb'):
    try:
        print 'writing proxy address to proxy.txt...'
        f=open('/home/carman/Desktop/proxy.txt',method)
        cnt=1
        for addr in prolist:
            f.write(addr+'\r\n')
            cnt+=1
        f.close
        print 'done'
    except Exception as e:
        print 'Excp: ',e

def main():
    sub=['nn','nt','wn','wt']
    for d in sub:
        for i in range(1,10):
            url='http://www.xicidaili.com/%s/%s'%(d,str(i))
            html=read_html(url)
            prolist=get_prolist(html)
            prolist=test_proxy(prolist)
            if d=='nn' and i==1:
                write_file(prolist) #clean old proxy list
            else:
                write_file(prolist,'ab')

if __name__=='__main__':
    main()
