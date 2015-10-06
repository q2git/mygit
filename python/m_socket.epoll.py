import socket
import select

rsp='hello world'
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

svrsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
svrsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
svrsock.bind(('127.0.0.1',8888))
svrsock.listen(1)
svrsock.setblocking(0)

epoll=select.epoll()
epoll.register(svrsock.fileno(),select.EPOLLIN)

try:
    cons={};reqs={};rsps={}
    while True:
        evns=epoll.poll(1)
        for fn,ev in evns:
            if fn==svrsock.fileno():
                csock,addr=svrsock.accept()
                csock.setblocking(0)
                epoll.register(csock.fileno(),select.EPOLLIN)
                cons[csock.fileno()]=csock
                reqs[csock.fileno()]=b''
                rsps[csock.fileno()]=rsp
            elif ev & select.EPOLLIN:
                reqs[fn]+=cons[fn].recv(1024)
                if EOL1 in reqs[fn] or EOL2 in reqs[fn]:
                    epoll.modify(fn,select.EPOLLOUT)
                    print('-'*40+'\n'+reqs[fn].decode())
            elif ev & select.EPOLLOUT:
                byteswritten=cons[fn].send[rsps[fn]]
                rsp[fn]=rsps[fn][byteswritten:]
                if len(rsps[fn])==0:
                    epoll.modify(fn,0)
                    cons[fn].shutdown(socket.SHUT_RDWR)
            elif ev & select.EPOLLHUP:
                epoll.unregister(fn)
                cons[fn].close()
                del cons[fn]
finally:
    epoll.unregister(svrsock.fileno())
    epoll.close()
    svrsock.close()
