import os
from time import gmtime,strftime,time
import datetime
import compressedclean
from socket import *
def file_size(filename):
	fp=open(filename)
	html_doc=fp.read()
	fp.seek(0, os.SEEK_END)
	file_size=fp.tell()
	return file_size
def overlap(ranges):
	if(len(ranges)>1):
		i = sorted(set([tuple(sorted(x)) for x in ranges]))
		f = [i[0]]
		for c, d in i[1:]:
			a, b = f[-1]
			if c<=b<d:
			    f[-1] = a, d
			elif b<c<d:
			    f.append((c,d))
			else:
			    pass
		return f
	else:
		return ranges
def read_data(ranges,filename,ent,gen):
	size=file_size(filename)
	m_flag=0
	data=""
	fp=open(filename)
	count=len(ranges)
	if(count>1):
		data="Content-type: multipart/byteranges; boundary=THIS_STRING_SEPARATES\n\n"	
		data+="--THIS_STRING_SEPARATES\n"
		data+="Content-type: {}".format(ent['Content-Type'])+"\n"
		data+="Content-Range:"+str(ranges[0][0])+"-"+str(ranges[0][1])+"/"+str(size)+"\n\n"
		m_flag=1
	for i in ranges:
			fp.seek(0,0)
			if(i is not None):
				if(i[0]!=0):
					fp.seek(i[0],1)
				if(count>1 and m_flag!=1):
					data+=" \n--THIS_STRING_SEPARATES\n"
					data+="Content-Type: {}".format(ent['Content-Type'])+"\n"
					data+="Content-Range:"+str(i[0])+"-"+str(i[1])+"/"+str(size)+"\n\n"
				data+=fp.read(i[1]-i[0]+1)
				data+="\n"
				m_flag=0
	if count==1:
		ent['Content-Range']= str(ranges[0][0])+"-"+str(ranges[0][1])+"/"+str(size)
	if(count>1):
		data+="\n--THIS_STRING_SEPARATES\n"
		ent['Content-Type']=''
		ent['Content-Range']='set'
	setlastmodified(filename,ent)
	return data
def setlastmodified(filename,ent):
	t=os.path.getmtime(filename)
	t=datetime.datetime.utcfromtimestamp(t)
	t=t.strftime("%a, %d %b %Y %H:%M:%S GMT") 
	ent['Last-Modified']="{}".format(t)
	size=file_size(filename)
	
def parseHeaders(filename,headerlist,headerdic,use):
	if(headerlist and use==''):
		hflag=0
		for i in range(len(headerlist)):
			#print headerlist[i]
			fieldname,value=headerlist[i].split(":",1)
			if fieldname=='Host' and hflag==0:
				hflag=1
			elif fieldname=='Host' and hflag==1:
				hflag=2
			headerdic[fieldname]=value.strip()
		if hflag==2:
			headerdic['Host']=''
	else:
		if use=='enco':
			aflag=0
			q=1
			limits={'identity':-2.0,'gzip':-2.0,'compress':-2.0,'deflate':-2.0}
			if(',' in headerdic['Accept-Encoding']):
				list1=headerdic['Accept-Encoding'].split(',')
				for x in list1:
					x=x.strip()
					if x[0]=='*':
						aflag=1
						if (';' in x):
							new=x.split(';')
							new1=new[1].split("=")
							q=new1[1]
					
					if( ';' in x):
						new=x.split(';')
						new[0]=new[0].strip()
						if(new[0] in limits):
							new1=new[1].split("=")
							new2=new1[1].strip()
							limits[new[0]]=float(new2)
					else:
						if x!='*' and x in limits:
							limits[x]=1.0
				if aflag==1:
					for i in limits:
						if limits[i]==-2.0:
							limits[i]=float(q.strip())
				
				if limits['identity']==-2.0:
					limits['identity']=1.0
			else:
				if(';' in headerdic['Accept-Encoding']):
						new=headerdic['Accept-Encoding'].split(';')
						new1=new[1].split("=")
						new2=new1[1]
						new[0]=new[0].strip()
						if new[0]!='*' and new[0]!='identity':
							limits[new[0]]=float(new[2].strip())
							limits['identity']=1.0
						elif new[0]=='*':
							for i in limits:
								limits[i]=float(new2.strip())
						elif new[0]=='identity':
							limits[new[0]]=float(new2.strip())
				else:
					if headerdic['Accept-Encoding']!='*':
						limits[headerdic['Accept-Encoding']]=1.0
						limits['identity']=1.0
					elif headerdic['Accept-Encoding']=='*':
						for i in limits:
							limits[i]=1.0
 					elif headerdic['Accept-Encoding']=='identity':
							limits['identity']=1.0
			return limits
		elif use=='auth' or use=='pauth':
			if use=='auth':
				index='Authorization'
			elif use=='pauth':
				index='Proxy-Authorization'
			if ('Basic' in headerdic[index]):
				cred=headerdic[index].split('Basic')
				cred=cred[1]
				try:
					cred = cred.encode("ascii") 
					cred = cred.decode("base64")
					cred = cred.decode("ascii") 
					if ':' in cred:
						cred=cred.split(':')
						un,pw=cred
					else:
						un='inv'
						pw='inv'
				except:
						un='inv'
						pw='inv'			
			else:
				un='inv'
				pw='inv'
			return un,pw
		elif use=='ch':
			sf=0
			qv=-2.0
			dictionary={'iso-8859-5':-2.0}	
			index='Accept-Charset'		
			if(',' in headerdic[index]):
				list1=headerdic[index].split(',')
				for x in list1:
					x=x.strip()
					if x[0]=='*':
						sf=1
					if( ';' in x):
						new=x.split(';')		
						new1=new[1].split("=")
						new2=new1[1]
						new[0]=new[0].strip()
						dictionary[new[0]]=float(new2.strip())
						if new[0]=='*':
							qv=dictionary[new[0]]
					else:
						dictionary[x]=1.0
						if x=='*':
							qv=1.0
				if sf==1 and dictionary['iso-8859-5']==-2.0:
					dictionary['iso-8859-5']=qv	
				elif sf==0 and dictionary['iso-8859-5']==-2.0:
					dictionary['iso-8859-5']=1.0
			else:
				if(';' in headerdic[index]):
						new=headerdic[index].split(';')
						if new[0]!='*':
							dictionary['iso-8859-5']=1.0
						new1=new[1].split("=")
						new2=new1[1]
						new[0]=new[0].strip()
						dictionary[new[0]]=float(new2.strip())
						if new[0]=='*':
							dictionary['iso-8859-5']=float(new2.strip())
				else:
					new=headerdic[index]
					new=new.strip()
					dictionary[new]=1.0
					dictionary['iso-8859-5']=1.0	
			return dictionary
		elif use=="split" or use=='lang':
			if use=='split':
				index='Accept'
			elif use=='lang':
				index='Accept-Language'
			dictionary={}			
			if(',' in headerdic[index]):
				list1=headerdic[index].split(',')
				for x in list1:
					x=x.strip()
					if( ';' in x):
						new=x.split(';')		
						new1=new[1].split("=")
						new2=new1[1]
						new[0]=new[0].strip()
						dictionary[new[0]]=float(new2.strip())
					else:
						dictionary[x]=1.0
			else:
				if(';' in headerdic[index]):
						new=headerdic[index].split(';')
						new1=new[1].split("=")
						new2=new1[1]
						new[0]=new[0].strip()
						dictionary[new[0]]=float(new2.strip())
				else:
					new=headerdic[index]
					new=new.strip()
		 			dictionary[new]=1.0	
		elif use=="range":
			index='Range'
			byte_range_set=[]
			size=file_size(filename)
			if(',' in headerdic[index]):
				for x in headerdic[index].split(','):
					if( "=" in x ):
						types=x.split("=")
						x=types[1]
						range_type=types[0]
					x=x.strip()
					if(x[0]!="-" and "-" in x):
							x=x.split("-")
							
							if(x[1]!="" and int(x[0].strip())<=int(x[1].strip()) and int(x[0].strip())<size):
								if(int(x[1].strip())<size):
									byte_range_set.append((int(x[0]),int(x[1])))
								else:
									byte_range_set.append((int(x[0]),size-1))
							else:
								if(x[1]=="" and int(x[0].strip())<size):
									byte_range_set.append((int(x[0].strip()),size-1))
					else:
						if( int(x.strip())<0):
							if( int(x.strip()) <0):
								if(abs(int(x))>size  and abs(int(x.strip()))>size):
									byte_range_set.append((0,size-1))
								else:
									byte_range_set.append((int(x.strip())+size,size-1))
			else:
				x=headerdic[index].split('=')
				range_type=x[0]
				x=x[1]
				if(x[0]!="-" and "-" in x):
					a,b=x.split('-')
					a=int(a.strip())
					if(b and int(b.strip())>=a and a<size):
						if(int(b.strip())<size):
							byte_range_set.append((a,int(b.strip())))
						else:
							byte_range_set.append((a,size))
					else:
						if not b: 
							if(size>a):
								byte_range_set.append((a,size-1))
				else:
					if( int(x.strip())<0):
						if( int(x.strip()) <0 and abs(int(x.strip()))>size):
							byte_range_set.append((0,size-1))
						else:
							byte_range_set.append((int(x.strip())+size,size-1))	
			ranges=overlap(byte_range_set)		
			return 	ranges				
		return dictionary
	
def error_3(code,filename,req,res,ent,gen,num):
	if code==301:
		et='Moved Permanently'
	elif code==302:
		et='Found'
	elif code==303:
		et='See Other'
	elif code==304:
		error_message=""
		error_message+="HTTP/1.1 "+'304 '+'Not Modified'+'\n'
		error_message+="Cache-Control: "+gen['Cache-Control']+'\n'+"Connection: "+gen['Connection']+'\n'+"Date: "+gen['Date']+'\n'+"Pragma: "+gen['Pragma']+'\n'
		error_message+="Server: "+res['Server']+'\n'+'\n'
		rv=error_message
		return rv
	elif code==307:
		et='Temporary Redirect'
	res['Retry-After']='5'
	ent['Content-Type']='text/html; charset=us-ascii'
	ent['Content-Language']='en'
	compressedclean.addmd5(filename,ent)
	t=os.path.getmtime(filename)
	t=datetime.datetime.utcfromtimestamp(t)
	t=t.strftime("%a, %d %b %Y %H:%M:%S GMT") 
	ent['Last-Modified']="{}".format(t)
	fp=open(filename)
	html_doc=fp.read()
	fp.seek(0, os.SEEK_END)
	file_size=fp.tell()
	error_message=""
	error_message+="HTTP/1.1 "+str(code)+' '+et+'\n'
	error_message+="Cache-Control: "+gen['Cache-Control']+'\n'+"Connection: "+gen['Connection']+'\n'+"Date: "+gen['Date']+'\n'
	error_message+="Location: "+res['Location']+'\n'+'Retry-After: '+res['Retry-After']+'\n'+"Server: "+res['Server']+'\n'
	if res['WWW-Authenticate']!='':
		error_message+="WWW-Authenticate: "+res['WWW-Authenticate']+'\n'
	if ent['Allow']!='':
		error_message+="Allow: "+ent['Allow']+'\n'
	error_message+="Content-Language: "+ent['Content-Language']+'\n'+"Content-Length: {}\n".format(file_size)+"Content-MD5: "+str(ent['Content-MD5']).strip()+'\n'+"Content-Type: "+ent['Content-Type']+'\n'+'\n'
	if num==1:
		rv=error_message
	else:
		rv=error_message+html_doc
	return rv
	
def error_4(code,filename,req,res,ent,gen,num):#all client errors start with 4
	content_range_flag=0
	ent['Content-Type']='text/html; charset=us-ascii'
	ent['Content-Language']='en'
	t=os.path.getmtime(filename)
	t=datetime.datetime.utcfromtimestamp(t)
	t=t.strftime("%a, %d %b %Y %H:%M:%S GMT") 
	ent['Last-Modified']="{}".format(t)
	compressedclean.addmd5(filename,ent)
	if code==400:
		et='Bad Request'
	elif code==401:
		et='Unauthorised'
	elif code==403:
		et='Forbidden'
	elif code==404:
		et='Not Found'
	elif code==405:
		et='Method Not Allowed'
		ent['Allow']='GET, POST, PUT, DELETE, HEAD'
	elif code==406:
		et='Not Acceptable'
	elif code==407:
		et='Proxy Authentication Required'
	elif code==408:
		et='Request Timeout'
	elif code==409:
		et='Conflict'
	elif code==411:
		et='Length Required'
	elif code==412:
		et='Precondition Failed'
	elif code==415:
		et='Unsupported Media Type'
	elif code==416:
		et="Requested range not satisfiable"
		content_range_flag=1
	elif code==417:
		et='Expectation Failed'
	elif code==501:
		et='Not Implemented'
	elif code==503:
		et='Service Unavailable'
	elif code==505:
		et='Version not supported'
	else:
		print("Code error")
		return('error')
	fp=open(filename)
	html_doc=fp.read()
	fp.seek(0, os.SEEK_END)
	file_size=fp.tell()
	error_message=""
	error_message+="HTTP/1.1 "+str(code)+' '+et+'\n'
	error_message+="Cache-Control: "+gen['Cache-Control']+'\n'+"Connection: "+gen['Connection']+'\n'+"Pragma: "+gen['Pragma']+'\n'+"Date: "+gen['Date']+'\n'
	if res['Retry-After']!='':
		error_message+='Retry-After: '+res['Retry-After']+'\n'
	error_message+="Server: "+res['Server']+'\n'
	if res['WWW-Authenticate']!='':
		error_message+="WWW-Authenticate: "+res['WWW-Authenticate']+'\n'
	if res['Proxy-Authenticate']!='':
		error_message+="Proxy-Authenticate: "+res['Proxy-Authenticate']+'\n'
	if ent['Allow']!='':
		error_message+="Allow: "+ent['Allow']+'\n'
	error_message+="Content-Language: "+ent['Content-Language']+'\n'+"Content-Length: {}\n".format(file_size)+"Content-MD5: "+str(ent['Content-MD5']).strip()+'\n'
	if(content_range_flag):
		error_message+="Content-Range:*\n"
	error_message+="Content-Type: "+ent['Content-Type']+'\n'+"Last-Modified: "+ent['Last-Modified']+'\n'+'\n'
	if num==1:
		rv=error_message
	else:
		rv=error_message+html_doc
	return rv
def success_200(code,filename,dictionary,res,ent,gen,ranges,num,cookie_dict,ip_Address):
	if code==200:
		compressedclean.addmd5(filename,ent)
		setlastmodified(filename,ent)
		fp=open(filename)
		html_doc=fp.read()
		fp.seek(0, os.SEEK_END)
		file_size=fp.tell()
		data=""
		data+="HTTP/1.1 200 OK\n"
		data+="Cache-Control: "+gen['Cache-Control']+'\n'+"Connection: "+gen['Connection']+'\n'+"Date: "+gen['Date']+'\n'
		data+="Server: "+res['Server']+'\n'
		if ent['Content-Encoding']!='identity':
			data+="Content-Encoding: "+ent['Content-Encoding']+'\n'
		if ent['Content-Language']!='':
			data+="Content-Language: "+ent['Content-Language']+'\n'
		data+="Content-Length: {}\n".format(file_size)
		if ent['Content-Location']:
			data+="Content-Location: "+ent['Content-Location']+'\n'
		data+="Content-MD5: "+str(ent['Content-MD5']).strip()+'\n'+"Content-Type: "+ent['Content-Type']+'\n'+"Last-Modified: "+ent['Last-Modified']+'\n'
		if(ip_Address in cookie_dict):
			data+=cookie_dict[ip_Address]+'\n'
		data+="\n"
		fp.seek(0)
		entity=fp.read()
		if num==1:
			rv=data+'\r\n\r\n'
		else:
			rv=data+entity
		return rv
	elif code==206:
		sflag=0
		data=""
		data+="HTTP/1.1 206 Partial Content"+'\n'
		if(ip_Address in cookie_dict):
			data+=cookie_dict[ip_Address]+'\n'
		data+="Cache-Control: "+gen['Cache-Control']+'\n'+"Connection: "+gen['Connection']+'\n'+"Pragma: "+gen['Pragma']+'\n'+"Date: "+gen['Date']+'\n'
		data+="Accept-Ranges:"+res['Accept-Ranges']+"\n"+"Server: "+res['Server']+'\n'
		if ent['Content-Encoding']!='identity':
			data+="Content-Encoding: "+ent['Content-Encoding']+'\n'
		if ent['Content-Language']!='':
			data+="Content-Language: "+ent['Content-Language']+'\n'
		data+="Content-Length: {}\n".format(len(filename))
		if ent['Content-Range']!='set':
			data+="Content-Range:"+ ent['Content-Range']+"\n"
			sflag=1
		if ent['Content-Type']!='':
			data+="Content-Type: "+ent['Content-Type']+'\n'
		data+="Last-Modified: "+ent['Last-Modified']+'\n'	
		
		if num==1:
			if ent['Content-Type']=='':
				data+="Content-type: multipart/byteranges; boundary=THIS_STRING_SEPARATES"	
			rv=data+'\r\n\r\n'
		else:
			if sflag==1:
				data+='\n'
			rv=data+filename
		return rv	
	elif code==201:
		data=""
		setlastmodified(filename,ent)
		data+="HTTP/1.1 201 Created"+"\n"
		data+="Cache-Control: "+gen['Cache-Control']+'\n'+"Connection: "+gen['Connection']+'\n'+"Pragma: "+gen['Pragma']+'\n'+"Date: "+gen['Date']+'\n'
		data+="Accept-Ranges:"+res['Accept-Ranges']+"\n"+"Server: "+res['Server']+'\n'
		data+="Location: http://localhost/"+res['Location']+"\n"
		data+="Last-Modified: "+ent['Last-Modified']+'\n'
		if(ip_Address in cookie_dict):
			data+=cookie_dict[ip_Address]+"\n"	
		data+="Content-Type: text/html\n"
		data+="<html> Your resource has been saved! Click <A href="+res['Location']+">here</A> to view it.</html>"
		data+="\r\n\r\n"
		rv=data
		return rv
	elif code==204:
		data=""
		data+="HTTP/1.1 204 No Content \n"
		data+="Cache-Control: "+gen['Cache-Control']+'\n'+"Connection: "+gen['Connection']+'\n'+"Pragma: "+gen['Pragma']+'\n'+"Date: "+gen['Date']+'\n'
		data+="Accept-Ranges:"+res['Accept-Ranges']+"\n"+"Server: "+res['Server']+'\n'
		if(ip_Address in cookie_dict):
			data+=cookie_dict[ip_Address]+"\n"
		data+="\r\n\r\n"	#204 should come with Etag,woh karna hai
		rv=data
		return rv	

	
