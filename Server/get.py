import os
import datetime
from time import gmtime,strftime
import codes
import compressedclean

def pathreturn(url,flag):
	path=(str(url).split("//"))
	if(path[0].lower()=="http:"):
		resource=path[1].split(":")
		if(len(resource)>1):
			rem=resource[1].split("/")
			flag=1
		else:
			rem=resource[0].split("/")
		if(rem[0].isdigit()):#if path is given
			port=rem[0]	
		else:
			port=1234
		rem=rem[1:]	
		filename=""
		for message in rem:
			filename=filename+"/"+message
		filename=filename[1:]
		paths=filename.split("?")
		if(len(paths)>1):
			query=paths[1]
		url='/'+paths[0]
	if url=='/':
		url='/index.html'
	return url[1:],flag
def checkcontentnego(filename,pathdic):
	f=open(pathdic['verpath'])
	f=f.read()
	if filename not in f:
		return 'N/A'
	else:
		return 'A'
	
def handleget(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num,pathdic,cookie_dict,address):
	f_flag=0
	flag=0
	try:
		filename,flag=pathreturn(message[1],flag)	
		filename1=str(pathdic['docpath'])+'/'+filename
		#print filename1
		f=open(filename1)
	except:
		loc,code=compressedclean.checkredirect(filename,pathdic)
		if loc!='N/A' and code!=000:
			resheadersdic['Location']=loc
			rv=codes.error_3(code,'confiles/error/'+str(code)+'.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv, str(code)
		#print filename1
		rv=codes.error_4(404,"confiles/error/404.html",reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return rv,'404'
	if len(message)>3:
		codes.parseHeaders("",headers[1:-2],reqheadersdic,'')
		#print reqheadersdic
	#print flag
	if ((reqheadersdic['Host']=='' or reqheadersdic['Host']!='localhost:1234') and flag==0):
		rv=codes.error_4(400,'confiles/error/400.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return rv,'400'
	un,pw,ty=compressedclean.checkprotect(filename,pathdic)
	if un!='N/A' and pw!='N/A' and reqheadersdic['Authorization']=='' and ty=='protect':
		resheadersdic['WWW-Authenticate']='Basic realm="Access to the protected file", charset="UTF-8"'
		rv=codes.error_4(401,'confiles/error/401.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return rv,'401'
	if un!='N/A' and pw!='N/A' and reqheadersdic['Authorization']!='' and ty=='protect':
		un1,pw1=codes.parseHeaders("","",reqheadersdic,'auth')
		#print un,pw
		if pw1!=pw:		
			rv=codes.error_4(403,'confiles/error/403.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv,'403'
	if un!='N/A' and pw!='N/A' and reqheadersdic['Proxy-Authorization']=='' and ty=='proxy':
		resheadersdic['Proxy-Authenticate']='Basic realm="Access to the protected file", charset="UTF-8"'
		rv=codes.error_4(407,'confiles/error/407.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return rv,'407'
	if un!='N/A' and pw!='N/A' and reqheadersdic['Proxy-Authorization']!='' and ty=='proxy':
		un1,pw1=codes.parseHeaders("","",reqheadersdic,'pauth')
		#print un,pw
		if pw1!=pw:		
			rv=codes.error_4(403,'confiles/error/403.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv,'403'
	#print(reqheadersdic)
	enco=priority=lang=chars={}
	ranges=[]
	
	if(reqheadersdic['Accept-Encoding']!=''):	
		enco=codes.parseHeaders("","",reqheadersdic,'enco') 	
	if(reqheadersdic['Accept']!=""):
		priority=codes.parseHeaders("","",reqheadersdic,'split')
	if(reqheadersdic['Accept-Language']!=""):
		lang=codes.parseHeaders("","",reqheadersdic,'lang')
	if(reqheadersdic['Accept-Charset']!=""):
		chars=codes.parseHeaders("","",reqheadersdic,'ch')	
	if(reqheadersdic['Range']!="" and reqheadersdic['If-Range']==""):
		ranges=codes.parseHeaders(filename1,"",reqheadersdic,"range")
	check=checkcontentnego(filename,pathdic)
	if check=='A':
		filen=compressedclean.contentnego(filename,reqheadersdic,resheadersdic,entheadersdic,enco,priority,lang,chars)
		if filen=='N/A':
			rv=codes.error_4(406,'confiles/error/406.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv,'406'
	if check=='N/A':
		filen=filename
	#print filen
	if filen!=filename:
		entheadersdic['Content-Location']=filen
	filen1=pathdic['docpath']+'/'+filen
	if reqheadersdic['If-Modified-Since']!='' and reqheadersdic['If-Unmodified-Since']=='' and reqheadersdic['If-Range']=='':
		dt=os.path.getmtime(filen1)
		date1=str(datetime.datetime.utcfromtimestamp(dt))
		given_date=str(datetime.datetime.strptime(reqheadersdic['If-Modified-Since'],'%a, %d %b %Y %H:%M:%S GMT'))
		if date1>given_date:
			rv=codes.success_200(200,filen1,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,ranges,num,cookie_dict,address)
			code='200'
		else:
			rv=codes.error_3(304,'',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv,'304'
		f_flag=1	
	if reqheadersdic['If-Unmodified-Since']!='' and reqheadersdic['If-Modified-Since']=='' and reqheadersdic['If-Range']=='':
		dt=os.path.getmtime(filen1)
		#print filen1
		date1=str(datetime.datetime.utcfromtimestamp(dt))
		given_date=str(datetime.datetime.strptime(reqheadersdic['If-Unmodified-Since'],'%a, %d %b %Y %H:%M:%S GMT'))
		#print date1
		if date1<given_date:
			rv=codes.success_200(200,filen1,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,'',num,cookie_dict,address)
			code='200'
		else:
			rv=codes.error_4(412,'confiles/error/412.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv,'412'
		f_flag=1
	if(reqheadersdic['Range']!=""):
		ranges=codes.parseHeaders(filen1,"",reqheadersdic,"range")
		if ranges==[]:
			rv=codes.error_4(416,'confiles/error/416.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv,'416'
		else:
			if reqheadersdic['If-Range']=='':
				entity=codes.read_data(ranges,filen1,entheadersdic,genheadersdic)
				rv=codes.success_200(206,entity,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,ranges,num,cookie_dict,address)
				code='206'
			elif reqheadersdic['If-Range']!='' and reqheadersdic['If-Unmodified-Since']=='' and reqheadersdic['If-Modified-Since']=='':
				dt=os.path.getmtime(filen1)
				date1=str(datetime.datetime.utcfromtimestamp(dt))
				given_date=str(datetime.datetime.strptime(reqheadersdic['If-Range'],'%a, %d %b %Y %H:%M:%S GMT'))
				if date1<given_date:
					entity=codes.read_data(ranges,filen1,entheadersdic,genheadersdic)
					rv=codes.success_200(206,entity,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,ranges,num,cookie_dict,address)
					code='206'
				else:
					rv=codes.success_200(200,filen1,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,'',num,cookie_dict,address)
					code='200'
		f_flag=1
	if(f_flag==0):
		rv=codes.success_200(200,filen1,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,'',num,cookie_dict,address)	
		code=200
	return rv,code
