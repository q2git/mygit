#coding:utf-8
import socket

host='127.0.0.1'
port=8888

#client TCP
def TCP(host,port):
    c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #c.setsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO,1)
    c.connect((host,port))
    while 1:
        msg=raw_input('>')
        if not msg:
            break
        c.send(msg) #send msg to server
        msg=c.recv(1024) #receive msg from server
        print '[%s:%d]: %s'%(host,port,msg)
    c.close()

def UDP(host,port):
    c=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    while True:
        msg=raw_input('>')
        if not msg:
            break
        c.sendto(msg,(host,port))
        msg=c.recv(100)
        if not msg:
            break
        print '[%s:%d]: %s'%(host,port,msg)
    c.close()
    
if __name__=='__main__':
    svrType=raw_input('1--TCP/2--UDP? :')
    #port=int(raw_input('Port:'))
    if svrType=='1':
        TCP(host,port)
    if svrType=='2':
        UDP(host,port)
