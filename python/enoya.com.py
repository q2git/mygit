# -*- coding: gb2312 -*-
#import urllib2,urllib,cookielib,re
from bs4 import BeautifulSoup
import threading,os,time,getpass,hashlib
from mylibs.discuz_login import *


#read web content
def read_url(opener,url,data=None):
    #HTTP heards
    user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;Mozilla Firefox 38.2.0 - 10792--72'
    header={'User-Agent':user_agent}
    req = urllib2.Request(url,data,header)
    html=''
    c=1 
    while not html:
        if c>10:break
        try:
            #print '->%s reading url "%s"...   '%(c,url[-30:]),
            html=opener.open(req,timeout=10).read()
            #print 'done.'
        except urllib2.HTTPError as e:
            html=''
            print 'HTTP Error: ',e.code,e.msg 
        except urllib2.URLError as e:
            html=''
            print 'URL Error: ',e.reason
        except Exception as e:
            html=''
            print
            print 'read error: ',e
        c=c+1
    return html

#analysis web content to get article links
def get_artlinks(html):
    links=[]
    soup = BeautifulSoup(html, 'lxml')
    marker=soup.find_all('a',class_='s xst') #use class_ due to class is reserved by python
    for link in marker:
        link=link.get('href')
        links.append(link)
        #print link
    return links

#analysis web content to get img links
def get_imglinks(html):
    links=[]
    soup = BeautifulSoup(html, 'lxml')
    marker=soup.find_all('img',zoomfile=re.compile(r'data.*?'))
    for link in marker:
        link='http://www.enoya.com/'+link.get('zoomfile')
        links.append(link)
        #print 'image link: %s'%str(link[-50:])
    return links

#download file
def download_data(opener,link,path):
    if not os.path.exists(path):os.mkdir(path) #mkdir if not exist
    data=read_url(opener,link) #read link
    fname=path+link.split('/')[-1]
    if data:
        write_file(fname,data)

#write data to file
def write_file(fname,data):
    #print '--> writing data to "%s"...   '%fname,
    try:
        f=open(fname,'wb')
        f.write(data)
        f.close
        print 'Done writing data to "%s"   '%fname
    except Exception as e:    
        print 'write error:',e
   
def main():
    website='http://www.enoya.com/'
    user=raw_input('Username:')
    psw=hashlib.md5(getpass.getpass('Password:')).hexdigest() #encrypted by MD5
#login websit
    opener=login_dz(username=user,password=psw,domain=website)
    print opener
    if not hasattr(opener,'open'):
        print 'login failed' 
        return 
    ###
    for i in range(3,11): #page 1 to 10
        #rp='http://www.enoya.com/finance-24-%s.html'%i
        rp='http://www.enoya.com/forum.php?mod=forumdisplay&fid=28&page='+str(i)
        print 'Page: %s'%rp[-50:]
        rootpage=read_url(opener,rp)
        artlinks=get_artlinks(rootpage)
        c=1
        for artlink in artlinks:
            print 'article No.: %s'%c,artlink[-30:0]
            html=read_url(opener,artlink)
            links=get_imglinks(html)
            cnt=0
            #download_data(opener,link,'img/'+str(i)+'/')
            thpool=[]
            for link in links:
                th=threading.Thread(target=download_data,
                                    args=(opener,link,'img/'+str(i)+'/'))
                thpool.append(th)
            for th in thpool:
                th.start()
                time.sleep(0.1)
            for th in thpool:
                th.join()
                
            c=c+1
    ###
            
if __name__ == "__main__":
    main()
