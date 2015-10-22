import urllib2,sqlite3
import os,time,types
import threading,Queue
from bs4 import BeautifulSoup

TESTRESULTS = []
URL_TEST = 'http://www.google.com'
HTTP_HEAD = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;Mozilla Firefox 38.2.0 - 10792--72'}
H_HTTP = urllib2.HTTPHandler(0)
LOCK = threading.Lock()
################################################################################
#get proxy addr from the Queue and test it
class Test(threading.Thread):
    def __init__(self,q_addr):
        threading.Thread.__init__(self)
        self.q_addr = q_addr
        self.testresults = []
        
    def run(self):
        global TESTRESULTS
        while True:
            proxy = self.q_addr.get()
            if proxy is None:self.q_addr.put(None);break
            self.test_proxy(proxy)
        LOCK.acquire()
        TESTRESULTS = TESTRESULTS + self.testresults
        LOCK.release()
        
    def test_proxy(self,proxy):
        host,port,ptype = proxy
        proxy={ptype:host+':'+port}
        h_proxy=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(h_proxy,H_HTTP)
        fails = 0
        t0 = time.time()
        while not(fails > 2):
            try:
                opener.open(URL_TEST,timeout=1).read(100)
                break
            except Exception as e:
                time.sleep(1)
                fails = fails + 1
                #print e
        speed = round(time.time() - t0,2)
        pf = ['PASS','FAIL'][fails>2]
        #(host,port,ptype,speed,pf)
        self.testresults.append((host,port,ptype,speed,pf))
        LOCK.acquire()
        print '%s-%s->%s %sED in %.2fs'%(self.getName(),os.getpid(),proxy,pf,speed)
        LOCK.release()

############################################################################
#read proxy list from url and return a list
def get_proxylist(url):
    proxylist = []
    try:
        print 'reading data from %s ...'%url,
        req = urllib2.Request(url,None,HTTP_HEAD)
        html = urllib2.urlopen(req,timeout=5).read()
        print 'Done.'      
        print 'analyzing web content ...',
        soup = BeautifulSoup(html,'html') 
        mark = soup.find_all('tr',class_=True)
        for item in mark:
            pros = (item.contents[5].string,
                    item.contents[7].string,
                    item.contents[13].string.lower())
            #print pros
            proxylist.append(pros)
        print 'Done.'
        return proxylist #['host:port type',...]
        
    except urllib2.HTTPError as e:
        print 'Http: ',e
    except urllib2.URLError as e:
        print 'Url: ',e
   # except Exception, e:
       # print e
        
#########################################################################
#########################################################################
def open_conn(db = r'/home/carman/Desktop/proxy.db'):
    table = ''
    if not os.path.exists(db):
        print 'Creating a new database in "%s" ...'%db
        table = '''create table if not exists PROXY(
            host varchar(50) primary key,
            port varchar(10),
            type varchar(10),
            speed float,
            pf varchar(10),
            ftimes integer,
            ptimes integer
            )'''
    conn = sqlite3.connect(db) 
    conn.isolation_level = None #auto commit()
    conn.execute(table)
    return conn    
############################
#item = [(host,port,type,speed,pf),()...]    
def db_update(items):   
    if type(items)!=types.ListType:
        print 'wrong type, List required.'
        return
        
    conn = open_conn()
    cur = conn.cursor()
    for item in items:
        if type(item)!=types.TupleType: 
            print 'wrong type, Tuple required.'
            break
        record = cur.execute("select host from PROXY where host=?",(item[0],)).fetchone()

        if record is None:
            print "Inserting new host %s ..."%item[0],
            cur.execute('insert into PROXY values(?,?,?,?,?,0,0)',(item))
            print 'Done.'
        else:
            print "Updating host %s ..."%item[0],
            if item[4] == 'PASS':
                cur.execute('update PROXY set port=?,type=?,speed=?,pf=?,ptimes=ptimes+1 where host=?',
                            (item[1],item[2],item[3],item[4],item[0]))
            elif item[4] == 'FAIL':
                cur.execute('update PROXY set port=?,type=?,speed=?,pf=?,ftimes=ftimes+1 where host=?',
                            (item[1],item[2],item[3],item[4],item[0]))
            print 'Done.'
                
    cur.close()
    conn.close()
#################################################################################        
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
###############################################################################
def main():
    t0 = time.time()    
    que_proxy = Queue.Queue()

    #read urls and get proxylist
    proxylist = []
    sub=['nn','nt','wn','wt']
    for d in sub:
        for i in range(1,11):
            url = 'http://www.xicidaili.com/%s/%s'%(d,str(i))
            proxylist = proxylist + get_proxylist(url)
    #read proxylist from database and combine into one

    #put proxy into a queue
    for item in proxylist:
        que_proxy.put(item)
    que_proxy.put(None) 
    print 'started to testing the proxies...'
    #start testing the proxy
    ths = []
    for x in xrange(20):
        th = Test(que_proxy)
        th.start()
        ths.append(th)
        #time.sleep(0.1)
        
    for th in ths:
        th.join()

    #que_proxy.join()

    print '-------------Test Report-------------'
    print 'Tested proxy: %d'%len(TESTRESULTS)
    print 'Passed proxy: %d'
    print 'Elapsed time: %.2fs'%(time.time()-t0)
    print TESTRESULTS
    ##write_file(lst)
    db_update(TESTRESULTS)
   
if __name__=='__main__':  
    main()
