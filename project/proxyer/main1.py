# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 11:19:45 2015

@author: carman
"""

import sys,threading,Queue
from PyQt4 import QtCore, QtGui
from mainwindow import Ui_mainWindow

        
class main(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.thread = Worker()
        self.addrs = []

        self.connect(self.thread, QtCore.SIGNAL("results(QString)"), self.updateTab)
    
    def loadpage(self,item):
        print item.text()
        self.ui.webView.setHtml(item.text())        
        
    def loadlist(self):
        i = 0
        tab = self.ui.table_main
        tab.setRowCount(len(LST))
        for item in LST:
            a1 = QtGui.QTableWidgetItem(item.split(' ')[0].strip())
            a2 = QtGui.QTableWidgetItem(item.split(' ')[1].strip())
            tab.setItem(i,0,a2)
            tab.setItem(i,1,a1)
            self.addrs.append(item+' '+ str(i))
            i = i+1       
 
    def testproxy(self):
        self.thread.do_job(self.addrs)
    
    def updateTab(self,results):
        r = str(results).split('-',3)
        print r[3]
        obj = self.ui.table_main
        rowid = int(r[0])
        pf = QtGui.QTableWidgetItem(r[2])
        t = QtGui.QTableWidgetItem(r[1])
        c = QtGui.QTableWidgetItem(r[3])
        obj.setItem(rowid,2,t)
        obj.setItem(rowid,3,pf)
        if r[2] == 'FAIL':
            obj.item(rowid,3).setForeground(QtGui.QColor(251, 0, 0))
        elif r[2] == 'PASS':
            obj.item(rowid,3).setForeground(QtGui.QColor(0,255,0))
        obj.setItem(rowid,4,c)

class Worker(QtCore.QThread):
    def __init__(self,parent = None):
        QtCore.QThread.__init__(self,parent)
        self.addr = None
        self.queue = Queue.Queue()
        
    def do_job(self,addrs):
        for addr in addrs:
            self.queue.put(addr)
        self.start()
    
    def run(self):
        print 'Strated'
        for x in xrange(50):
            th = threading.Thread(target=self.testing)
            th.start()
        #self.testing(self.queue.get())
        
    def testing(self):
        while True:
            addr = self.queue.get()
            import urllib2,time
            rowid = addr.split(' ')[2]
            proxy={addr.split(' ')[1].strip():addr.split(' ')[0].strip()}
            #print proxy
            h_proxy=urllib2.ProxyHandler(proxy)
            opener=urllib2.build_opener(h_proxy)
            fails = 0
            results = rowid + '-...-Testing...-...' 
            self.emit(QtCore.SIGNAL("results(QString)"),results)
            t0 = time.time()
            while not(fails > 2):
                try:
                    response=opener.open('http://www.baidu.com',timeout=5).read()
                    results = 'PASS' +'-' + response
                    break
                except Exception as e:
                    results = 'FAIL' + '-' + str(e)
                    fails = fails + 1
            t1 = time.time() 
            results = rowid + '-' + str(t1-t0) + '-'+results
            #print results        
            self.emit(QtCore.SIGNAL("results(QString)"),results)          
                
if __name__ == '__main__':
    global LST 
    LST = []
    f = open('proxy.txt','r')
    while True:
        l = f.readline()
        if not l: break
        LST.append(l)
    #print LST
    
    app = QtGui.QApplication(sys.argv)
    myapp = main()
    myapp.show()
    sys.exit(app.exec_())
    
