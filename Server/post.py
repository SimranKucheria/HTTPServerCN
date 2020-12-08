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

def handlepost(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,data,pathdic,cookie_dict,address):
	num=0
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
			if code==301 or code==302:
				code=303
			rv=codes.error_3(code,'confiles/error/'+str(code)+'.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv, str(code)
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
	f=open("post.txt",'w')
	f.write(data)
	rv=codes.success_200(204,filename1,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,'',num,cookie_dict,address)
	return rv,'204'
