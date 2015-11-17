# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:44:38 2015

"""
import pyodbc
import glob,time,subprocess,shutil
import threading, Queue

uid=raw_input('Please input user ID:')
pwd=raw_input('Password:')
#SQL
strConn = "DRIVER={SQL Server};SERVER=ip;DATABASE=db;UID=%s;PWD=%s;"%(uid,pwd)

class Worker(threading.Thread):
    def __init__(self, wid, q_req,lock,startdirs):
        threading.Thread.__init__(self)
        self.wid = wid
        self.que = q_req
        self.lock = lock
        self.startdirs = startdirs
        self.start() #start self

    def run(self):
        srvdir = "\\\\ip\\DocSrv"
        t0 = time.time()  
        while 1:
            msg = ""
            if self.que.qsize() == 0:break
            data = self.que.get()  
            idx,reqdoc = data
            result = self._findPQI(reqdoc+'*.pdf')           
            fn = result.split('\\') #'file name'
            try:
                #update servermsg in database
                with pyodbc.connect(strConn).cursor() as c:
                    c.execute("update [docserver] set servermsg=? where id=?",(fn[-1],idx)) 
                #copy request doc to srvdir    
                if not result in ['NOT_FOUND','MUL_FOUND']:
                    #subprocess.Popen(['xcopy', result, srvdir,'/Q/D/C/Y'])
                    shutil.copy(result,srvdir)
                msg = '\\'.join(fn[-2:])
            except Exception as e:
                msg = e
                #break
            self.que.task_done()
            with self.lock:
                print '[WORKER%s-%s]: %s'%(self.wid,idx,msg)
        #worker job done
        t1 = time.time() 
        with self.lock:
            print '*** Worker%s finished in %.2fSec ***'%(self.wid,(t1-t0))
    
    def _findPQI(self,PQI):
        for d in self.startdirs:
            fp = glob.glob(d.strip()+PQI) 
            if len(fp) == 1:
                return fp.pop()
            elif len(fp) > 1:
                return 'MUL_FOUND'            
        return 'NOT_FOUND'



def main():
    q_req = Queue.Queue()
    lock = threading.Lock()
    startdirs = open('doc_path.txt','rb').readlines()
    strsql = "Select id,requestdoc,clientinfo from [docserver] where servermsg='PENDING'"
    print 'Doc Server is Runing...'
    while 1:
        msg = ""
        workers = 0
        t0 = time.time()
        #polling request from db
        try:
            with pyodbc.connect(strConn).cursor() as c:
                c.execute(strsql)
                if c.rowcount != 0:
                    for idx,reqdoc,client in c:
                        q_req.put((idx,reqdoc))
                        print '[%s-%s]: %s'%(client,idx,reqdoc)

        except Exception as e:
            time.sleep(60)
            msg = e    
            
        #launch workers
        workers = int((q_req.qsize()-1)/20)+1
        for x in xrange(workers):
            Worker(x,q_req,lock,startdirs)
        time.sleep(10)
        #block untile all previous tasks done
        q_req.join()  
        t1 = time.time()
        with lock:
            print '*** Server assigned %s worker(s) and serviced for %.2fSec ***'%(workers,(t1-t0))
            print msg
           

            
if __name__ == '__main__':
    main()
