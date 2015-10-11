# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sun Oct 11 19:34:03 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(797, 627)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.table_main = QtGui.QTableWidget(self.centralwidget)
        self.table_main.setMinimumSize(QtCore.QSize(0, 200))
        self.table_main.setMaximumSize(QtCore.QSize(16777215, 500))
        #self.table_main.setSizeAdjustPolicy(QtGui.QAbstractScrollArea.AdjustIgnored)
        self.table_main.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_main.setWordWrap(False)
        self.table_main.setCornerButtonEnabled(False)
        self.table_main.setObjectName(_fromUtf8("table_main"))
        self.table_main.setColumnCount(5)
        self.table_main.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.table_main.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_main.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_main.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_main.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_main.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_main.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(251, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.table_main.setItem(0, 3, item)
        self.table_main.horizontalHeader().setDefaultSectionSize(150)
        self.table_main.horizontalHeader().setMinimumSectionSize(50)
        self.table_main.horizontalHeader().setStretchLastSection(True)
        self.table_main.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.table_main, 0, 0, 1, 3)
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setMinimumSize(QtCore.QSize(0, 300))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 1, 0, 1, 3)
        self.pb_load = QtGui.QPushButton(self.centralwidget)
        self.pb_load.setMinimumSize(QtCore.QSize(0, 50))
        self.pb_load.setObjectName(_fromUtf8("pb_load"))
        self.gridLayout.addWidget(self.pb_load, 2, 0, 1, 1)
        self.pb_test = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_test.sizePolicy().hasHeightForWidth())
        self.pb_test.setSizePolicy(sizePolicy)
        self.pb_test.setMinimumSize(QtCore.QSize(0, 50))
        self.pb_test.setObjectName(_fromUtf8("pb_test"))
        self.gridLayout.addWidget(self.pb_test, 2, 1, 1, 1)
        self.pb_exit = QtGui.QPushButton(self.centralwidget)
        self.pb_exit.setMinimumSize(QtCore.QSize(0, 50))
        self.pb_exit.setObjectName(_fromUtf8("pb_exit"))
        self.gridLayout.addWidget(self.pb_exit, 2, 2, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 797, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QObject.connect(self.pb_exit, QtCore.SIGNAL(_fromUtf8("clicked()")), mainWindow.close)
        QtCore.QObject.connect(self.pb_test, QtCore.SIGNAL(_fromUtf8("clicked()")), mainWindow.testproxy)
        QtCore.QObject.connect(self.pb_load, QtCore.SIGNAL(_fromUtf8("clicked()")), mainWindow.loadlist)
        QtCore.QObject.connect(self.table_main, QtCore.SIGNAL(_fromUtf8("itemClicked(QTableWidgetItem*)")), mainWindow.loadpage)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "ProxyTester", None))
        self.table_main.setSortingEnabled(False)
        item = self.table_main.verticalHeaderItem(0)
        item.setText(_translate("mainWindow", "test", None))
        item = self.table_main.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "Type", None))
        item = self.table_main.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "Address", None))
        item = self.table_main.horizontalHeaderItem(2)
        item.setText(_translate("mainWindow", "Elapsed", None))
        item = self.table_main.horizontalHeaderItem(3)
        item.setText(_translate("mainWindow", "Status", None))
        item = self.table_main.horizontalHeaderItem(4)
        item.setText(_translate("mainWindow", "Comment", None))
        __sortingEnabled = self.table_main.isSortingEnabled()
        self.table_main.setSortingEnabled(False)
        item = self.table_main.item(0, 3)
        item.setText(_translate("mainWindow", "FAIL", None))
        self.table_main.setSortingEnabled(__sortingEnabled)
        self.pb_load.setText(_translate("mainWindow", "Load Proxy", None))
        self.pb_test.setText(_translate("mainWindow", "Test Proxy", None))
        self.pb_exit.setText(_translate("mainWindow", "Exit", None))

from PyQt4 import QtWebKit
