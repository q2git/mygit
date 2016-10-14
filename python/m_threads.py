import threading,Queue
import time,random

#producer thread
class Producer(threading.Thread):
    def __init__(self,que,que2,lock):
        threading.Thread.__init__(self)
        self.queue = que
        self.que2 = que2
        self.lock = lock
        self.start()

    def run(self):
        while 1:
            n = self.queue.get() #block untile get data
            if n:
                with self.lock:
                    print 'Producer ',self.getName(),'adding',n,'to queue'
                self.que2.put(n+0.1)
                time.sleep(1)
            else:               
                break
            
        self.queue.put(None)  #for other threads to exit    
        with self.lock:
            print 'Producer ',self.getName(),' Stopped.'             


#consumer thread
class Consumer(threading.Thread):
    def __init__(self,que2,lock):
        threading.Thread.__init__(self)
        self.queue = que2
        self.lock = lock
        self.start()
        
    def run(self):
        while 1:
            n = self.queue.get() #block untile get data
            if n:
                with self.lock:
                    print 'Consumer ',self.getName(),' got a value:',n
                time.sleep(1)
            else:           
                break
            
        self.queue.put(None)  #for other threads to exit             
        with self.lock:
            print 'Consumer ',self.getName(),' Stopped,'                


#main thread
def main():
    que = Queue.Queue()
    que2 = Queue.Queue()
    lock = threading.Lock()
    
    map(que.put, range(1,10))
    que.put(None) #end tag
    
    ths_p = []
    for th in xrange(1):
        ths_p.append(Producer(que, que2, lock))
    
    ths_c = []    
    for th in xrange(1):
        ths_c.append(Consumer(que2, lock))
        
    for th in ths_p:
        th.join()
        
    que2.put(None) #for Consumter to stop
 
    for th in ths_c:
        th.join()
        
    print 'All tasks done.'
        



if __name__ == '__main__':
    main()
    
            
