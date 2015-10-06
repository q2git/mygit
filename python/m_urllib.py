import urllib
import urllib2
import cookielib

#redirect handler
class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        print "301"
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        print "302"
        pass
    
url='http://www.ti.com'
#HTTP heards
user_agent='Mozilla/5.0 (Windows NT 6.1; \
WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;\
Mozilla Firefox 38.2.0 - 10792--72'
headers={'User-Agent':user_agent}
request=urllib2.Request(url,None,headers)
#cookie handler
cookie=cookielib.CookieJar()
cookie_handler=urllib2.HTTPCookieProcessor(cookie)
#password handler
psw=urllib2.HTTPPasswordMgrWithDefaultRealm()
psw.add_password(None,url,'user','psw')
psw_handler=urllib2.HTTPBasicAuthHandler(psw)
#proxy handler
proxy={'http':'http://110.154.15.202:8080'}
proxy_handler=urllib2.ProxyHandler(proxy)
#http/https handler
http_handler = urllib2.HTTPHandler(debuglevel=1)
https_handler = urllib2.HTTPSHandler(debuglevel=1)
#build opener
opener=urllib2.build_opener(proxy_handler,
                            cookie_handler)
                            #http_handler,
                            #https_handler)
                            #RedirectHandler)
#urllib2.install_opener(opener)

try:
    #response=urllib2.urlopen(request)
    response=opener.open(request)
    #content=response.read()
    #print content
except urllib2.HTTPError as e:
    print 'HTTP Error: ',e.code,e.msg 
except urllib2.URLError as e:
    print 'URL Error: ',e.reason

else:
    print 'No exception was raised.'
    print response.geturl()
    print response.info()
    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value
