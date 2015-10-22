# -*- coding: utf-8 -*-

import sqlite3
import os,types

############################
def open_conn(db = r'D:\mydata.db'):
    table = ''
    if not os.path.exists(db):
        print 'Creating a new database in "%s" ...'%db
        table = '''create table if not exists PROXY(
            host varchar(50) primary key,
            port varchar(10),
            type varchar(10),
            speed varchar(10),
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

############################  
if __name__ == '__main__':    
    items=[('10.10.11.12','8888','http','3.5s','PASS'),('10.10.10.12','8888','http','3.5s','PASS')]
    db_update(items)
