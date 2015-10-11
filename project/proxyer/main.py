# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:58:06 2015

@author: 
"""

import sys

from PyQt4 import QtCore, QtGui
from listview import Ui_PorxyList

class startQt4(QtGui.QMainWindow):
    def __init__(self,LST,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_PorxyList()
        self.ui.setupUi(self)
        self.list = LST
        
        QtCore.QObject.connect(self.ui.tabWidget,QtCore.SIGNAL('currentChanged(int)'),
                               self.tab_change)
        QtCore.QObject.connect(self.ui.treeList,QtCore.SIGNAL('itemClicked(QTreeWidgetItem*,int)'),
                               self.list_selected)                       
        QtCore.QObject.connect(self.ui.bt_start,QtCore.SIGNAL('clicked()'),
                               self.btstart)        
        #all proxy list
        self.tab_change(0)
    
    def btstart(self):
        it = QtGui.QTreeWidgetItemIterator(self.ui.treeList)
        it
        while it.value():
            #print it.value().text(1),it.value().text(0)
            it += 1
        
         
    def list_selected(self,item,index):
        print item.text(1),index,QtCore.QModelIndex(self.ui.treeList.indexFromItem(item)).row()
    def tab_change(self,tab_id):
        txt = ''
        
        if tab_id == 0:
            b = self.ui.treeList
            txt = 'TESTING'
            c = QtGui.QColor(0,0,0)
        elif tab_id == 1:
            b = self.ui.treeList_P
            txt = 'PASS' 
            c = QtGui.QColor(0,255,0)
        elif tab_id ==2:
            b = self.ui.treeList_F
            txt = 'FAIL'
            c = QtGui.QColor(255,0,0)
        
        b.clear() #clear all content
        b.setColumnWidth(0,85)
        b.setColumnWidth(1,150)
        b.setColumnWidth(2,100)
        b.setColumnWidth(2,100) 
        
        cnt = 0
        for item in self.list: 
            t = item.split(' ')
            if t[2].strip() == txt:
                cnt += 1
                a = QtGui.QTreeWidgetItem(b)
                a.setText(0,t[1].strip())
                a.setText(1,t[0].strip())
                a.setText(2,t[2].strip())
                a.setTextColor(2, c)
                a.setText(3,str(cnt))

            
if __name__ == '__main__':
    LST = []
    f = open('proxy.txt','r')
    while True:
        l = f.readline()
        if not l: break
        LST.append(l)
    #print LST
    
    app = QtGui.QApplication(sys.argv)
    myapp = startQt4(LST)
    myapp.show()
    sys.exit(app.exec_())
    
