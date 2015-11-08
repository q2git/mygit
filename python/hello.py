import urllib2
import codecs

response = urllib2.urlopen('http://guba.eastmoney.com/list,600596.html')
data = response.read()
with codecs.open('test.html','wb') as f:
    f.write(data)
