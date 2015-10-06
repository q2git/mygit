import pyodbc


#uid=raw_input('Please input user ID:')
#pwd=raw_input('Password:')
#SQL
#strConn = "DRIVER={SQL Server};SERVER=xx.xx.xx.xx;DATABASE=xx;UID=%s;PWD=%s;"%(uid,pwd)
#Access 
strConn = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s" %('D:\xxx.mdb')

conn = pyodbc.connect(strConn)

strsql = "Select top 10 * from [Table]"

c=conn.cursor()
c.execute(strsql)
#print c.fetchone()
#print c.fetchall()
#print c.fetchmany(5)
for row in c:
    print row.ID
    
c.close()
conn.close()
