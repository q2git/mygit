# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:44:38 2015
"""
import pyodbc
import glob,time,os
import threading, Queue
from shutil import copy

uid=raw_input('Please input user ID:')
pwd=raw_input('Password:')
#SQL
strConn = "DRIVER={SQL Server};SERVER=xxx;DATABASE=xxx;UID=%s;PWD=%s;"%(uid,pwd)

def req_monitor(q_req,lock):
    strsql = "Select id,requestdoc,clientinfo from [docserver] where servermsg='PENDING'"
    while 1:
        with pyodbc.connect(strConn).cursor() as c:
            c.execute(strsql)
            if c is not None:
                for idx,reqdoc,client in c:
                    q_req.put((idx,reqdoc))
                    with lock:
                        print '[%s-%s]: %s'%(client,idx,reqdoc)
                    #q_req.put(None)
                #threading.Thread(target=req_handle, args=(q_req,lock)).start()
        #with lock:
        #    print 'sleep 10s for next polling...'
        time.sleep(10)


def req_handle(q_req,lock):
    svrdir = "xxx"
    while 1:    
        data = q_req.get()
        if data is None: break
        t0 = time.time()    
        idx,reqdoc = data
        result = find_PQI(reqdoc+'*.pdf')
        fn = result.split('\\') #'file name'
        if not result in ['NOT_FOUND','MUL_FOUND']:
            if not os.path.exists(svrdir+fn[-1]):
                #print 'copying...',result
                copy(result,svrdir)
   
        with pyodbc.connect(strConn).cursor() as c:
            c.execute("update [docserver] set servermsg=? where id=?",(fn[-1],idx))
        t1 = time.time()    
        with lock:
            print '[SERVER-%s]: %s in %.2fSec'%(idx,'\\'.join(fn[-2:]),(t1-t0))


def find_PQI(PQI):
    startdirs = open('doc_path.txt','rb').readlines()
    for d in startdirs:
        fp = glob.glob(d.strip()+PQI) 
        if len(fp) == 1:
            return fp.pop()
        elif len(fp) > 1:
            return 'MUL_FOUND'            
    return 'NOT_FOUND'
  
def main():
    q_req = Queue.Queue()
    lock = threading.Lock()
    
    #req_monitor(q_req,lock)
    #monitor thread
    monitor = threading.Thread(target=req_monitor, args=(q_req,lock))
    monitor.start()
    
    #handler thread
    handler = threading.Thread(target=req_handle, args=(q_req,lock))
    handler.start() 
    
    #block here
    monitor.join()
    handler.join()
    
            
if __name__ == '__main__':
    main()
    
#doc_path.txt
'''Z:\xxx\xxx\'''
#sql db table
'''
Create table [dbo].[docserver](
id int identity(1,1) primary key,
date datetime DEFAULT getdate(),
requestdoc varchar(100),
servermsg varchar(50) DEFAULT  'PENDING',
clientmsg varchar(50) DEFAULT  'PENDING',
clientinfo varchar(200)
)
'''
#vba cdoe (client)
'''
'***********************************************************
'*************************Get PQI***************************
'***********************************************************
Function Get_PQI(PQI As String)
    Dim Reqid, Filename, ClientMsg, Response
    
    SrvDir = CFG_links(0) & "DocSrv\"
    LocalDir = CFG_links(1) + CFG_floor + "\DocSrv\"
    ClientInfo = Get_ComputerName()
    
    '1. send doc request to server
    On Error GoTo Err_handler   'error handle
    Call Open_Conn
    objConn.Execute ("insert into [docserver] (requestdoc,clientinfo) values('" + PQI + "','" + ClientInfo + "')")
    Reqid = objConn.Execute("Select SCOPE_IDENTITY()").GetString()
    '2. sleep 10 sec for response from server
    ClientMsg = "FAIL"
    For i = 10 To 0 Step -1
        RepairDocs.scaninput.Text = "[wait " + str(i) + "sec...]"
        DoEvents
        Sleep 1500
        Response = Trim(objConn.Execute("select servermsg from [docserver] where id=" + Reqid).GetString(, , , " "))
        Filename = Response
        Select Case Response
        Case "NOT_FOUND", "MUL_FOUND"
            ClientMsg = "ABORT"
            Exit For
        Case Else
            If Dir(LocalDir + Filename) <> "" Then
                ClientMsg = "DONE"
                Exit For
            ElseIf Dir(SrvDir + Filename) <> "" Then
                ClientMsg = "DONE"
                str_cp = "XCOPY """ + SrvDir + Filename + """ """ + LocalDir + """ /C/S/E/Y"
                Call Excute_Shell("" + str_cp, 0)
                Sleep 1000
                Exit For
            End If
        End Select
    Next
    '3. update db-clientmsg and open file
    objConn.Execute ("update [docserver] set clientmsg='" + ClientMsg + "' where id=" + Reqid)
    If ClientMsg = "DONE" Then Call Excute_Shell("" + LocalDir + Filename, 0)
    RepairDocs.scaninput.Text = "[" + Response + "]"
    
Err_handler:
    If Err.Number <> 0 Then
        MsgBox Err.description, vbExclamation
    End If
    Call Close_Conn
End Function
'''
