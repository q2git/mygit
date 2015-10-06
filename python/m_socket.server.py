import socket
import select

class CS:
    def __init__(self,addr):
        self.addr=addr
        self.srvsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.srvsock.bind(addr)
        self.srvsock.listen(5)
        self.descriptors=[self.srvsock]
        print 'ChatServer started on [%s:%s]' %(addr[0],addr[1])

    def run(self):
        while 1:
            #await an event on a readable socket descriptor
            (sread,swrite,sexc)=select.select(self.descriptors,[],[])
            #iterate through the tagged read descriptors
            for sock in sread:
                if sock==self.srvsock:
                    self.accept_new_connection()
                else:
                    try:
                        str=sock.recv(100)
                    except:
                        str=''
                    if str=='':
                        host,port=sock.getpeername()
                        str='Client left %s:%s' %(host,port)
                        self.broadcast_string(str,sock)
                        sock.close
                        self.descriptors.remove(sock)
                    else:
                        host,port=sock.getpeername()
                        newstr='[%s:%s] %s' %(host,port,str)
                        self.broadcast_string(newstr,sock)
                        

    def broadcast_string(self,str,omit_sock):
        for sock in self.descriptors:
            if sock != self.srvsock and sock!=omit_sock:
                try:
                    sock.send(str)
                except:
                    print 'Socket error.'
        print str

    def accept_new_connection(self):
        newsock,(remhost,remport)=self.srvsock.accept()
        #self.srvsock.setblocking(0) #non-blocking mode
        self.descriptors.append(newsock)
        newsock.send("You're connected to the Server")
        str='Client joined %s:%s' %(remhost,remport)
        self.broadcast_string(str,newsock)
        
if __name__ == '__main__': 
    #if raw_input('Local?:')=='no':
    #    host=socket.gethostbyname(socket.getfqdn())
    #else:
    host='127.0.0.1'
    addr=(host,8888)    
    myCS=CS(addr).run()

