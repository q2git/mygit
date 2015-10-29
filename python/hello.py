item={}
def x():
    for i in range(10):
        yield {item['a']:(i,i+1),item['b']:i*3}
    
a= x()

for i in a:
    print i[0]