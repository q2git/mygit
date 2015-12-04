# -*- coding: utf-8 -*-
import pyodbc
import glob,time,subprocess
import threading, Queue
import sys
from PyQt4 import QtGui,QtCore

uid=raw_input('Please input user ID:')
pwd=raw_input('Password:')
#SQL
strConn = "DRIVER={SQL Server};SERVER=xxx;DATABASE=xxx;UID=%s;PWD=%s;"%(uid,pwd)
startdirs = open('doc_path.txt','rb').readlines()

class Worker(threading.Thread):
    def __init__(self, wid, q_req,msg):
        threading.Thread.__init__(self)
        self.wid = wid
        self.que = q_req
        self.msg = msg
        self.startdirs = startdirs
        self.start() #start self

    def run(self):
        srvdir = "\\\\xxx\\DocSrv"
          
        while 1:
            t0 = time.time()
            info = ""
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
                    subprocess.Popen(['xcopy', result, srvdir,'/Q/D/C/Y'])
                    #shutil.copy(result,srvdir)
                info = '\\'.join(fn[-2:])
            except Exception as e:
                info = e
                #break
            self.que.task_done()
            t1 = time.time() 
            self.msg.insertItem(0,'%s [W%s-%s]: %s in %.2fsecs'%(time.strftime("%Y-%m-%d %H:%M:%S"),self.wid,idx,info,(t1-t0)))
            #if len(self.msg)>100: self.msg.pop()
        #worker job done
        #self.msg.insert(0,'***WORKER%s Done***'%self.wid)
        
    def _findPQI(self,PQI):
        for d in self.startdirs:
            fp = glob.glob(d.strip()+PQI) 
            if len(fp) == 1:
                return fp.pop()
            elif len(fp) > 1:
                return 'MUL_FOUND'            
        return 'NOT_FOUND'
  

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.initUI()
        
    def initUI(self):
        self.que = Queue.Queue()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timeout)
    
        self.list1 = QtGui.QListWidget(self)
        self.list2 = QtGui.QListWidget(self)
        hspliter = QtGui.QSplitter(2,self)
        hspliter.addWidget(self.list1)
        hspliter.addWidget(self.list2)
        self.btn = QtGui.QPushButton('Start Server')
        self.btn.setMinimumHeight(50)
        self.btn.clicked.connect(self.btnClicked)
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(hspliter)
        vbox.addWidget(self.btn)
        
        self.setLayout(vbox)
        self.setWindowTitle('Docuement Server')
        self.setGeometry(10,680,500,300)
        self.show()
        
    def btnClicked(self):      
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start Server')
            self.list1.insertItem(0,time.strftime("%Y-%m-%d %H:%M:%S")+' Server Stoped')
        else:
            self.timer.start(1000*10)
            self.btn.setText('Stop Server')
            self.list1.insertItem(0,time.strftime("%Y-%m-%d %H:%M:%S")+' Server Started')

    def timeout(self):
        self.list1.setEnabled(not self.list1.isEnabled())
        self.list2.setEnabled(not self.list1.isEnabled())
        if self.que.qsize() != 0: return #avoid duplication
        try:
            with pyodbc.connect(strConn).cursor() as c:
                c.execute("Select id,requestdoc,clientinfo from [docserver] where servermsg='PENDING'")
                if c.rowcount != 0:
                    for idx,reqdoc,client in c:
                        self.que.put((idx,reqdoc)) #put into queue
                        self.list1.insertItem(0,time.strftime("%Y-%m-%d %H:%M:%S")+' ['+client +']:'+ reqdoc)
                    #process requests
                    workers = int((self.que.qsize()-1)/20)+1
                    for x in xrange(workers):
                        Worker(x,self.que,self.list2) 
        except Exception as e:
            self.list1.insertItem(0,"%s error:%s"%(time.strftime("%Y-%m-%d %H:%M:%S"),e))


def main():  
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
