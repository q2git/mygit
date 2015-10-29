# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:02:26 2015
"""
import glob, codecs, types, os, time
import pyodbc
from bs4 import BeautifulSoup

#######################################################################
def db_query(sql):
    uid= raw_input('Please input user ID:')
    pwd= raw_input('Password:')   
    strConn = "DRIVER={SQL Server};SERVER=10.54.152.14;DATABASE=MFO;\
                UID=%s;PWD=%s;"%(uid,pwd)
    #Access 
    #strConn = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};\
    #            DBQ=%s" %('D:\RIS.mdb')
    
    with pyodbc.connect(strConn).cursor() as c:
        c.execute(sql)     
        records = c.fetchall()
        return records

#######################################################################
def mk_script(SAPParts):
    if type(SAPParts) != types.ListType:
        print 'wrong type, list required.' 
        return 
    wd = 'D:\\01_GuiXT\\VBA\\'
    print 'Generating script in "%s" ...'%wd,
    with codecs.open(wd+'Script_Templet.txt','rb','utf_8_sig' ) as f,\
        codecs.open(wd+'Script.txt','wb','utf_8_sig') as fw:
        templet = f.read()
        for SAPPart in SAPParts:
            t = templet.replace('999999999',SAPPart)
            fw.write(t)
            
        with codecs.open(wd+'end_script.txt','rb','utf_8_sig' ) as fend:
            fw.write(fend.read())  
    print 'Done.'

#######################################################################
def run_script():
    cmd_checkSAP = 'tasklist /FI "IMAGENAME eq SAP*"'
    cmd_checkGuiXT = 'tasklist /FI "IMAGENAME eq guixt*"'
    cmd_Kill = "Taskkill /F /IM  SAP* /T"
    param = '''\SAP\FrontEnd\SAPgui\sapshcut.exe  -sysname="P27: Production PDM [Public]" -client=011 -user=xxx -password=xxx -Language=E '''   
    cmd_SAP = 'C:\progra~2%s'%param
    cmd_Script = r'''C:\progra~2\sap\frontend\sapgui\guixt.exe Input="OK: process=D:\01_GuiXT\VBA\Script.txt" '''
    cmd_Script = cmd_Script + '&&cmd.exe'
    
    if 'No tasks' in os.popen(cmd_checkSAP).read() or \
    'SUCCESS' in os.popen(cmd_Kill).read():
        os.popen(cmd_SAP).read()

    print 'Sleep 15sec for SAP starting up...',
    time.sleep(15)
    print 'Done'
    
    if not 'No tasks' in os.popen(cmd_checkSAP).read():
        print 'Excuting the GuiXT script...'
        os.popen(cmd_Script).read()
        while not 'No tasks' in os.popen(cmd_checkGuiXT).read():
            print '*',
            time.sleep(1)
        print '\nDone.'
        return True
    else:
        print 'SAP failed to start, please retry!'
        return False

#######################################################################
def get_desc(flist = None):
    if flist is None:
        flist = glob.glob(r'D:\02_BOMs\*.HTM')
    else:
        flist = map(lambda x:'D:\\02_BOMs\\'+str(x[0])+'.HTM',flist )

    for fp in flist:
        with open(fp,'r') as f:           
            soup = BeautifulSoup(f.read(5000))
            try:
                #item1 = soup.find('nobr',attrs={'id':'l0001022'}).get_text()
                item = soup.find('nobr',attrs={'id':'l0002022'}).get_text()
            except:
                 item = soup.find('nobr',attrs={'id':'l0004022'}).get_text()               
            #SAPPart,Description
            yield (fp[fp.rfind('\\')+1:fp.find('.')],item.strip())

#######################################################################
def db_update(items):
    #SAPPart,Description,Area,Foler
    uid= raw_input('Please input user ID:')
    pwd= raw_input('Password:')   
    strConn = "DRIVER={SQL Server};SERVER=10.54.152.14;DATABASE=MFO;\
                UID=%s;PWD=%s;"%(uid,pwd)

    raw_input('please enter to update database...')
    
    with pyodbc.connect(strConn).cursor() as c:
        for item in items:
            record = c.execute("select SAPPart from [tab_Product] where SAPPart=?",(item[0],)).fetchone()
            if record is None:
                print 'inserting [%s %s]'%item
                c.execute('insert into [tab_Product] (SAPPart,Description) values(?,?)',item)
            else:
                print 'updating [%s %s]'%item
                c.execute('update [tab_Product] set Description=? where SAPPart=?',(item[1],item[0]))                
        c.commit()
    print 'Database [tab_Product] has been updated.'

#######################################################################
def upload_bom():
    print os.popen('D:\\02_BOMs\\CopyToServer.BAT').read()
         
#######################################################################
def main():
    records = db_query("Select SAPPart from [View_WIPs] group by SAPPart" )
    nodescs = db_query("Select SAPPart from [View_WIPs] where Description is null group by SAPPart" )
        
    mk_script(map(lambda x:x[0],records))
    run_script()
    
    items = get_desc(nodescs)
    db_update(items)
    
    upload_bom()
        
    
#######################################################################   
if __name__ == '__main__':
    main()
 
#######################################################################   
#Script_Templet.txt (UTF-8)
'''
Screen SAPLSMTR_NAVIGATION.0100
  Enter "ys12"
Screen SAPLY27S_BOM_CSL.0100
  Set F[Material] 	"999999999"
  Set F[Alternative BOM] 	"1"
  Set F[BOM Application] 	"pp01"
  Enter "/5"      
Screen SAPLY27S_BOM_CSL.0105
  Set C[Disp Subitems] 	"X"
  Enter "=YUPS"
Screen SAPLY27S_BOM_CSL.0105
  Set C[Classification] 	"X"
  Enter "/8"      
Screen SAPLSLVC_FULLSCREEN.0500
  Enter "/45"      	
Screen SAPLSPO5.0110
  Set R[HTML Format] 	"X"
  Enter
Screen SAPLSFES.0200
  Set F[Directory] 	"D:\02_BOMs"
  Set F[File Name] 	"999999999.HTM"
  Enter "/11"      
Screen SAPLSLVC_FULLSCREEN.0500
  Enter "/n" 
'''
#end_script.txt UTF-8
'''
Screen SAPLSMTR_NAVIGATION.0100
  Enter "/15"
// Log Off 
Screen SAPLSPO1.0100
  Enter "=YES"  
'''
#CopyToServer.BAT
'''
copy "D:\02_BOMs\*.HTM"  "\\10.54.152.14\Test pro\RepairData\Temp\BOMs\" & Move "D:\02_BOMs\*.HTM" "D:\02_BOMs\BACKUP"
'''
