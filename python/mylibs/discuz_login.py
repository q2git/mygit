# -*- coding: gb2312 -*-
import urllib2,urllib,cookielib,re
 
'''
 ͨ�õĵ�½DZ��̳
 ����˵��parms:
   username:�û���(����),
   password :����(����),
   domain:��վ������ע���ʽ�����ǣ�http://www.xxx.xx/(����),
   answer:�����,
   questionid:����ID,
   referer:��ת��ַ
    
 ����ʹ���˿ɱ�ؼ��ֲ���(�����Ϣ�ɲο��ֲ�)
'''
def login_dz(**parms):
 
  #��ʼ��
  parms_key = ['domain','answer','password','questionid','referer','username']
  arg = {}
  for key in parms_key:
    if key in parms:
      arg[key] = parms[key]
    else:
      arg[key] = ''
  #HTTP heards
  user_agent=r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0)Gecko/20100101 Firefox/38.0;Mozilla Firefox 38.2.0 - 10792--72'
  header=[('User-Agent',user_agent)]       
  #cookie����
  cookieFile = './discuz_cookies.dat'
  cookie = cookielib.LWPCookieJar()
  opener = urllib2.build_opener(urllib2.HTTPHandler(1),urllib2.HTTPCookieProcessor(cookie))
  opener.addheaders = header
  
  #��ȡformhash
  pre_login = arg['domain']+'member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
  c = opener.open(pre_login).read()
  cookie.save(cookieFile)
  patt = re.compile(r'.*?name="formhash".*?value="(.*?)".*?')
  formhash = patt.search(c)
  if not formhash:
    raise Exception('GET formhash Fail!')
  formhash = formhash.group(1)
 
  #��½
  postdata = {
   'answer':arg['answer'],
   'formhash':formhash,
   'password':arg['password'],
   'questionid':0 if arg['questionid']=='' else arg['questionid'],
   'referer':arg['domain'] if arg['referer']=='' else arg['referer'],
   'username':arg['username'],
    }
 
  postdata = urllib.urlencode(postdata)
  req = urllib2.Request(
    url= arg['domain']+'member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LCaB3&inajax=1',
    data=postdata
    )
  c = opener.open(req).read()
  
  readback(c)
  flag = '��½ʧ�� %s'%arg['username']
  if 'succeedhandle_login' in c:
      flag = opener
  return flag

#write proxy list to a text file
def readback(data):
    try:
        print 'writing data to readback.html...'
        f=open('readback.html','w')
        f.write(data)
        print 'done'
    except Exception as e:
        print 'Excp: ',e 
    finally:
        f.close()
 
#ʹ�����ӣ�����������½
'''
user=''
pwd=''
dom='http://www.enoya.com/' #��һ��������վ��http://bbs.jb51.net/
try:
    flag = login_dz(username=user,password=pwd,domain=dom)
    print(flag)

    a=flag.open(r'http://www.enoya.com/forum.php?mod=viewthread&tid=4110910&extra=page%3D1')
    print 'writing data to ...   ',
    f=open('img/temp.htm','wb')
    f.write(a.read())
    f.close
    print 'done.'

except Exception,e:
  print('Error:',e)
'''
