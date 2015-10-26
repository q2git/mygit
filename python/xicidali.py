import urllib2,sqlite3
import os,time
import threading,Queue
from bs4 import BeautifulSoup

TESTURLS = ['http://www.baidu.com','http://www.google.com']
HTTP_HEAD = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;Mozilla Firefox 38.2.0 - 10792--72'}
H_HTTP = urllib2.HTTPHandler(0)
LOCK = threading.Lock()
################################################################################
#get proxy addr from the Queue and test it
class Test(threading.Thread):
    def __init__(self,que_proxy,que_results):
        threading.Thread.__init__(self)
        self.q_addr = que_proxy
        self.q_results = que_results
        
    def run(self):
        global TESTRESULTS
        while True:
            proxy = self.q_addr.get()
            if proxy is None:self.q_addr.put(None);break
            self.test_proxy(proxy)
        
    def test_proxy(self,proxy):
        host,port,ptype = proxy
        proxy={ptype:host+':'+port}
        h_proxy=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(h_proxy,H_HTTP)
        fails = [0,0]
        speeds =[0,0]
        for i in range(2):
            speeds[i] = time.time()
            while not(fails[i] > 2):
                try:
                    opener.open(TESTURLS[i],timeout=1).read(100)
                    break
                except Exception as e:
                    #time.sleep(1)
                    fails[i] = fails[i] + 1
                    #print e
            speeds[i] = time.time() - speeds[i]

        pf = ['PASS','FAIL'][fails[0]>2] #baidu
        fq = ['PASS','FAIL'][fails[1]>2] #google
        #(host,port,ptype,speed,pf)
        self.q_results.put((host,port,ptype,round(speeds[0],2),pf,
                                 round(speeds[1],2),fq))
        LOCK.acquire()
        print '%s-%s->%s %sED. %d left'%(self.getName(),os.getpid(),proxy,pf,self.q_addr.qsize())
        LOCK.release()

############################################################################
#read proxy list from url and put into a queue
def get_proxylist(que_urls,que_proxy):
    while 1:
        url = que_urls.get()
        if url == None: break
        retry = 0
        while retry<2:
            try:
                with LOCK:
                    print 'reading data from %s ...'%url
                req = urllib2.Request(url,None,HTTP_HEAD)
                html = urllib2.urlopen(req,timeout=5).read()
                #print 'Done.'      
                with LOCK:
                    print 'analyzing web content ...'
                soup = BeautifulSoup(html,'html') 
                mark = soup.find_all('tr',class_=True)
                for item in mark:
                    pros = (item.contents[5].string,
                            item.contents[7].string,
                            item.contents[13].string.lower())
                    #print pros
                    que_proxy.put(pros)
                #print 'Done.' 
                break
            except Exception, e:
                print e
            retry += 1
            time.sleep(2)

        
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
            speed1 float,
            pf varchar(10),
            speed2 float,
            fq varchar(10)
            )'''
    conn = sqlite3.connect(db) 
    conn.isolation_level = None #auto commit()
    conn.execute(table)
    return conn    
############################
#item = [(host,port,type,speed1,pf,speed2,fq),()...]    
def db_update(que_results):   
    conn = open_conn()
    cur = conn.cursor()
    while 1:
        item = que_results.get()
        if item == None: que_results.put(None);break
            
        record = cur.execute("select host from PROXY where host=?",(item[0],)).fetchone()
        if record is None:
            with LOCK:
                print "Inserting new host %s ..."%item[0]
            cur.execute('insert into PROXY values(?,?,?,?,?,?,?)',(item))
            #print 'Done.'
        else:
            with LOCK:
                print "Updating host %s ..."%item[0]
            #pftimes = 'ptimes=ptimes+1' if item[4]=='PASS' else 'ftimes=ftimes+1'
            keys = list(item);  keys.append(keys.pop(0))
            cur.execute('update PROXY set port=?,type=?,speed1=?,pf=?,speed2=?,fq=? where host=?',(tuple(keys)))
                        #(item[1],item[2],item[3],item[4],item[0]))
            #print 'Done.'           
    cur.close()
    conn.close()
    print 'all tested proxies have been updated to database.'
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

def write_txt(que_results):
    print 'writing proxy address to proxy.txt...'
    with open('/home/carman/Desktop/proxy.txt','wb') as f1,\
            open('/home/carman/Desktop/list.txt','wb') as f2:
        while 1:
            item = que_results.get()
            if item == None: que_results.put(None);break
            if item[4]=='PASS':
                f2.write(item[2]+r'://'+item[0]+':'+item[1]+'\n')
                if item[6]=='PASS': f1.write(item[0]+' '+item[1]+' '+item[2]+'\n')  
    print 'all passed proxies have been written to file.'
###############################################################################
def main(): 
    que_urls = Queue.Queue()
    que_proxy = Queue.Queue()
    que_resutls = Queue.Queue()
    #put urls into a queue
    sub=['nn','nt','wn','wt']
    for d in sub:
        for i in range(1,2):
            url = 'http://www.xicidaili.com/%s/%s'%(d,str(i))
            que_urls.put(url)
    que_urls.put(None)
    
    print 'started to getting proxy list...'
    th0 = threading.Thread(target=get_proxylist, args=(que_urls,que_proxy))
    th0.start()    
    
    time.sleep(5)
    print 'started to testing the proxies...'
    ths = []
    for x in xrange(10):
        th = Test(que_proxy,que_resutls)
        th.start()
        ths.append(th)
    
    time.sleep(5)   
    #write results to database and text files    
    th1 = threading.Thread(target=db_update,args=(que_resutls,))
    th1.start()
    th2 = threading.Thread(target=write_txt,args=(que_resutls,))
    th2.start() 
    
    th0.join()
    print 'all proxies have been got from web.'
    que_proxy.put(None) 
    
    for th in ths:
        th.join()
    print 'all proxies have been tested.' 
    que_resutls.put(None)
    
    th1.join()
    th2.join()
    print 'all tasks done.'

   
if __name__=='__main__':  
    main()
