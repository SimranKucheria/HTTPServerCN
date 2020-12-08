from socket import *
from time import gmtime,strftime,time
import get
import codes
import threading
import put
import post
import Cookie
import datetime
import delete
import ForFiles
from random import randint
from time import sleep

serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
cookie_dict={}
def set_cookie(ip):
	dictionary={}
	random_list=[]
	global cookie_dict
	if(cookie_dict):
		for i in cookie_dict:
			list1=cookie_dict[i].split("expires=")
			random=list1[0].split("session=")
			num=random[1].split(";")
			random_list.append(int(num[0].strip()))
			present=datetime.datetime.now()
			present=present.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
			present=str(datetime.datetime.strptime(present,'%a, %d-%b-%Y %H:%M:%S GMT'))
			given_time=str(datetime.datetime.strptime(list1[1].strip(),'%a, %d-%b-%Y %H:%M:%S GMT'))
			if(given_time<=present):
				continue
			dictionary[i]=cookie_dict[i]
	#print(random_list)
	cookie_dict=dictionary
	expiration = datetime.datetime.now() + datetime.timedelta(minutes=30)
	cookie = Cookie.SimpleCookie()
	cookie["session"] = randint(0,1000000000)
	cookie["session"]["domain"] = ".localhost"
	cookie["session"]["expires"] = \
	expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
	while(ip not in cookie_dict and cookie["session"] in random_list):
			cookie["session"] = random.randint(0,1000000000)
	if(ip not in cookie_dict):
		cookie_dict[ip]=cookie.output()
def writealog(pathdic,addr,logtime,code,size,request=''):
	lock = threading.Lock()
	lock.acquire()
	alog=str(pathdic['alogpath'])
	f=open(alog,'a+')
	string=str(addr[0])+' '+'['+logtime+']'+' '+request+' '+str(code)+' '+str(size)+'\n'
	f.write(string)
	lock.release()

def writelog(pathdic,addr,logtime,request=''):
	lock = threading.Lock()
	lock.acquire()
	elog=str(pathdic['elogpath'])
	f=open(elog,'a+')
	string=str(addr[0])+' '+'['+logtime+']'+' '+request+'\n'
	f.write(string)
	lock.release()

def recvdata(clientSocket,address,date,pathdic):
	clientSocket.settimeout(1000)
	message=''
	CRLF='\r\n\r\n'
	while True:
            try:
                data = clientSocket.recv(1)
                if data:
                    message+= data.decode()
		if message and CRLF in message:
		    return message	
	    except timeout:
		rv=codes.error_4(408,"confiles/error/408.html",reqheadersdic,resheadersdic,entheadersdic,genheadersdic,0)
		writealog(pathdic,address,date,'408',len(rv))
		clientSocket.sendall(rv)
		#Canputsleep	
		clientSocket.close()
		break
	    except:
                continue
def getcl(reqMess):
	mess=reqMess.split('\n')
	for m in mess:
		if 'Content-Length' in m:
			m=m.split(':')
			m=m[1]
			m.split()
			return int(m)
def getdata(clientSocket,n,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,address,pathdic,date):
	num=n
	message=''
	while True:
            try:
                data = clientSocket.recv(1)
                if data:
                    message+= data.decode()
		if len(message)==int(num):
		    return message	
	    except timeout:
		rv=codes.error_4(408,"confiles/error/408.html",reqheadersdic,resheadersdic,entheadersdic,genheadersdic,0)
		writealog(pathdic,address,date,'408',len(rv))
		clientSocket.sendall(rv)	
		clientSocket.close()
		break
	    except:
                continue
	
def server(clientSocket,address,pathdic):
	try:
		#clientSocket,address=serverSocket.accept()
		reqheadersdic={'Accept':'','Accept-Charset':'','Accept-Encoding':'',
	'Accept-Language':'','Authorization':'','Expect':'','From':'','Host':'','Range':'','If-Modified-Since':'','If-Range':'',
	'If-Unmodified-Since':'','Proxy-Authorization':'','TE':'','User-Agent':'','Allow':'','Content-Encoding':'','Content-Language':'','Content-Length':'','Content-Location':'','Content-MD5':'','Content-Range':'','Content-Type':'','Last-Modified':''}
		#Headers covered are Accept, Accept-Charset,Accept-Encoding,Accept-Language,AUthorization,From,Host,Range,If-Modified-Since,If-Range,If-Unmodified-Since,Proxy-Authorization,User-Agent
		resheadersdic={'Accept-Ranges':'bytes','Age':'','Location':'','Proxy-Authenticate':'','Retry-After':'','Server':'HTTP Server','Vary':'','WWW-Authenticate':''}
		#Headers coverec are Accept-Ranges,Proxy-Authenticate,Retry-After,Server,WWW-Authenticate
		entheadersdic={'Allow':'','Content-Encoding':'','Content-Language':'','Content-Length':'','Content-Location':'','Content-MD5':'','Content-Range':'','Content-Type':'','Last-Modified':''}
		#Headers covered are Allow,Content-Encoding,Content-Language,Content-Location,Content-MD5,Content-Range,Content Length,Content Type,Connection,Last Modified
		genheadersdic={'Cache-Control':'no-cache','Connection':'close','Date':'','Pragma':'no-cache','Trailer':'','Transfer-Encoding':'','Upgrade':'','Via':'','Warning':''}
		#Headers covered are Cache-Control,Connection,Date,Pragma
		set_cookie(address[0])
		date=strftime("%a, %d %b %Y %H:%M:%S GMT",gmtime()) 
		genheadersdic['Date']="{}".format(date)
		reqMess=str(recvdata(clientSocket,address,date,pathdic))
		#print reqMess
		if reqMess==None:
			#Canputsleep
			clientSocket.close()
			return
		message=reqMess.split()
		headers=reqMess.split("\n")
		if message[0]=='HEAD':
			num=1
		else: 
			num=0
		if len(message)<3:
			rv=codes.error_4(400,"confiles/error/400.html",reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			string='"'+headers[0][:-1]+'"'
			writealog(pathdic,address,date,'400',len(rv),string)
			clientSocket.sendall(rv)
			#Canputsleep	
			clientSocket.close()
			return
		if(message[2] and message[2][:5]=="HTTP/" and message[2]!="HTTP/1.1") :
			rv=codes.error_4(505,"confiles/error/505.html",reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			string='"'+headers[0][:-1]+'"'
			writealog(pathdic,address,date,'505',len(rv),string)
			clientSocket.sendall(rv)
			#Canputsleep	
			clientSocket.close()
			return
		if(message[2]!="HTTP/1.1") :
			rv=codes.error_4(400,"confiles/error/400.html",reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			string='"'+headers[0][:-1]+'"'
			writealog(pathdic,address,date,'400',len(rv),string)
			clientSocket.sendall(rv)
			#Canputsleep	
			clientSocket.close()
			return
		if(message[0] not in ['GET','POST','HEAD','DELETE','PUT','TRACE','CONNECT','OPTIONS']):
			rv=codes.error_4(405,'confiles/error/405.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			string='"'+headers[0][:-1]+'"'
			clientSocket.sendall(rv)
			writealog(pathdic,address,date,'405',len(rv),string)
			#Canputsleep	
			clientSocket.close()
			return
		if(message[0] in ['TRACE','CONNECT','OPTIONS']):
			rv=codes.error_4(501,'confiles/error/501.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			string='"'+headers[0][:-1]+'"'
			clientSocket.sendall(rv)
			writealog(pathdic,address,date,'501',len(rv),string)
			#Canputsleep	
			clientSocket.close()
			return
		if(message[0]=="GET"):
			rv,code=get.handleget(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num,pathdic,cookie_dict,address[0])
			string='"'+headers[0][:-1]+'"'
			clientSocket.sendall(rv)
			writealog(pathdic,address,date,code,len(rv),string)
			#Canputsleep	
			#print rv
			clientSocket.close()		
			return
		if(message[0]=="HEAD"):
			rv,code=get.handleget(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num,pathdic,cookie_dict,address[0])
			string='"'+headers[0][:-1]+'"'
			clientSocket.sendall(rv)
			writealog(pathdic,address,date,code,len(rv),string)
			#Canputsleep	
			clientSocket.close()		
			return
		if(message[0]=="PUT"):
			if 'Expect' in reqMess:
				if 'Content-Length' not in reqMess:
					string='"'+headers[0][:-1]+'"'
					rv=codes.error_4(417,'confiles/error/417.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
					clientSocket.sendall(rv)
					writealog(pathdic,address,date,'417',len(rv),string)
					#Canputsleep
					clientSocket.close()
					return
				if 'Content-Length' in reqMess:
					lock = threading.Lock()
					lock.acquire()
					code,rv=put.handleexpect(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,pathdic,address[0])
					lock.release()
					clientSocket.sendall(rv)
					if code==417:
						string='"'+headers[0][:-1]+'"'
						writealog(pathdic,address,date,'417',len(rv),string)
						#Canputsleep
						clientSocket.close()
						return
				string='"'+headers[0][:-1]+'"'
				writealog(pathdic,address,date,'100',20,string)
			if 'Content-Length' not in reqMess:
					string='"'+headers[0][:-1]+'"'
					rv=codes.error_4(411,'confiles/error/411.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
					clientSocket.sendall(rv)
					writealog(pathdic,address,date,'411',len(rv),string)
					#Canputsleep
					clientSocket.close()
					return
			dlen=getcl(reqMess)
			data=getdata(clientSocket,int(dlen),reqheadersdic,resheadersdic,entheadersdic,genheadersdic,address,pathdic,date)
			#print dlen	
			#print data
			lock = threading.Lock()
			lock.acquire()
			rv,code =put.handleput(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,data,pathdic,cookie_dict,address[0])
			lock.release()
			string='"'+headers[0][:-1]+'"'
			clientSocket.sendall(rv)
			writealog(pathdic,address,date,code,len(rv),string)
			#Canputsleep
			clientSocket.close()
			return
		if(message[0]=="DELETE"):
			lock = threading.Lock()
			lock.acquire()
			rv,code= delete.handledelete(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num,pathdic,cookie_dict,address[0])
			lock.release()	
			string='"'+headers[0][:-1]+'"'
			clientSocket.sendall(rv)
			writealog(pathdic,address,date,code,len(rv),string)
			#Canputsleep	
			clientSocket.close()	
			return	
		if(message[0]=="POST"):
			if 'Content-Length' not in reqMess:
					string='"'+headers[0][:-1]+'"'
					rv=codes.error_4(411,'confiles/error/411.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
					clientSocket.sendall(rv)
					writealog(pathdic,address,date,'411',len(rv),string)
					#Canputsleep
					clientSocket.close()
					return
			dlen=getcl(reqMess)
			data=getdata(clientSocket,int(dlen),reqheadersdic,resheadersdic,entheadersdic,genheadersdic,address,pathdic,date)
			lock = threading.Lock()
			lock.acquire()
			rv,code=post.handlepost(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,data,pathdic,cookie_dict,address[0])
			string='"'+headers[0][:-1]+'"'
			lock.release()	
			clientSocket.sendall(rv)
			writealog(pathdic,address,date,code,len(rv),string)
			#Canputsleep	
			clientSocket.close()	
			return	
	except:
		try:
			string='"'+headers[0][:-1]+'"'
		except:
			string="Unexpected Error"
		clientSocket.sendall("Unexpected Error")
		writelog(pathdic,address,date,string)
		#Canputsleep
		clientSocket.close()
serverPort=1234
serverSocket.bind(('localhost',serverPort))		
f=open('confiles/server.conf')
s=f.read()
s=s.split('\n')
s=s[2:]
pathdic={}
for conf in s:
	if 'DocumentRoot' in conf:
		m=conf.split(':')
		pathdic['docpath']=m[1]
	elif 'AcessLog' in conf:
		m=conf.split(':')
		pathdic['alogpath']=m[1]
	elif 'ErrorLog' in conf:
		m=conf.split(':')
		pathdic['elogpath']=m[1]
	elif 'Redirectlist' in conf:
		m=conf.split(':')
		pathdic['rlpath']=m[1]
	elif 'Protectedlist' in conf:
		m=conf.split(':')
		pathdic['plpath']=m[1]
	elif 'Versions' in conf:
		m=conf.split(':')
		pathdic['verpath']=m[1]
	elif 'Max Simultaneous connections' in conf:
		m=conf.split(':')
		msc=int(m[1])

serverSocket.listen(msc)
print "Getting Server Ready....."
ForFiles.new(pathdic)
print "Server Running"
while True:
	conn, addr = serverSocket.accept()
        t=threading.Thread(target = server,args = (conn,addr,pathdic))
	t.start()
	#t.join()


