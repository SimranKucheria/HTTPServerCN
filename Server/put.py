import os
import datetime
from time import gmtime,strftime
import codes
import compressedclean
import magic
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
def check_var(filename,reqheadersdic,mime_type,pathdic):
	charset=[]
	name=filename.split('.',1)
	f=open("confiles/varfile/"+name[0]+".var","a+")
	lines=f.readlines()
	#print(lines)
	if(len(lines)==1):
		f=open(pathdic['verpath'],"a+")
		actualname=lines[0].split(";")
		f.write(actualname[1])
	f=open("confiles/varfile/"+name[0]+".var","a+")
	if(reqheadersdic['Content-Encoding']==""):
		f.write("identity:")
	else:
		f.write(reqheadersdic['Content-Encoding']+":")
	if(reqheadersdic['Content-Type']==""):
		f.write(mime_type+":")
	else:
		if(";" in reqheadersdic['Content-Type']):
			type=reqheadersdic['Content-Type'].split(";")
			charset=type[1].split("=")
			f.write(type[0]+":")
		else:
			f.write(reqheadersdic['Content-Type']+":")
	if(reqheadersdic['Content-Language']==""):
		if(len(mime_type)>=6 and mime_type[0:6]!="image/"):
			f.write("en:")
		else:
			f.write("i:")
	else:
		f.write(reqheadersdic['Content-Language']+":")
	if(charset):
		f.write(charset[1]+";")
	else:
		if(len(mime_type)>=6 and mime_type[0:6]!="image/"):
			f.write("iso-8859-5;")	
		else:
			f.write("i;")
	f.write(filename+"\n")	
def check_existing_var(filename,reqheadersdic,mime_type):
	charset=[]
	name=filename.split('.',1)
	f=open("confiles/varfile/"+name[0]+".var","a+")
	charac=f.readlines()
	new_list=[]
	for i in charac:
		line=i.split(";")
		#print len(line)
		if(len(line)>=2 and line[1].strip("\n")==filename):
			
			if(reqheadersdic['Content-Encoding']==""):
				line[0]="identity"+":"
			else:
				line[0]=reqheadersdic['Content-Encoding']+":"
			if(reqheadersdic['Content-Type']==""):
				line[0]+=mime_type+":"
			else:
				if(";" in reqheadersdic['Content-Type']):
					type=reqheadersdic['Content-Type'].split(";")
					charset=type[1].split("=")
					line[0]+=(type[0]+":")
				else:
					line[0]+=reqheadersdic['Content-Type']+":"
			if(reqheadersdic['Content-Language']==""):
				if(len(mime_type)>=6 and mime_type[0:6]!="image/"):
					line[0]+="en:"
				else:
					line[0]+="i:"
			else:
				line[0]+=reqheadersdic['Content-Language']+":"
			if(charset):
				line[0]+=charset[1]+';'
			else:
				if(len(mime_type)>=6 and mime_type[0:6]!="image/"):
					line[0]+="iso-8859-5;"
				else:
					line[0]+="i;"
			line[0]+=filename+"\n"
			
			new_list.append(line[0])
		else:
			new_list.append(i)
	#print(new_list)
	file1 = open("confiles/varfile/"+name[0]+".var", 'w') 
	file1.writelines(new_list) 
def handleput(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,data,pathdic,cookie_dict,address):
	f_flag=0
	flag=0
	newfileflag=0
	num=0
	try:
		filename,flag=pathreturn(message[1],flag)
		filename1=str(pathdic['docpath'])+'/'+filename
		f=open(filename1)
	except:
		loc,code=compressedclean.checkredirect(filename,pathdic)
		if loc!='N/A' and code!=000:
			resheadersdic['Location']=loc
			if code==301 or code==302:
				code=307
			rv=codes.error_3(code,'confiles/error/'+str(code)+'.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv, str(code)
		newfileflag=1
	if len(message)>3:
		codes.parseHeaders("",headers[1:-2],reqheadersdic,'')
	if ((reqheadersdic['Host']=='' or reqheadersdic['Host']!='localhost:1234') and flag==0):
		rv=codes.error_4(400,'confiles/error/400.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return rv,'400'
	if reqheadersdic['Last-Modified']!='' and newfileflag==0:
		dt=os.path.getmtime(filename1)
		date1=str(datetime.datetime.utcfromtimestamp(dt))
		given_date=str(datetime.datetime.strptime(reqheadersdic['Last-Modified'],'%a, %d %b %Y %H:%M:%S GMT'))
		if date1>given_date:
			rv=codes.error_4(409,'confiles/error/409.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv,'409'
	un,pw,ty=compressedclean.checkprotect(filename,pathdic)
	if un!='N/A' and pw!='N/A' and ty=='protect' and reqheadersdic['Authorization']=='' and newfileflag==0:
		resheadersdic['WWW-Authenticate']='Basic realm="Access to the protected file", charset="UTF-8"'
		rv=codes.error_4(401,'confiles/error/401.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return rv,'401'
	if un!='N/A' and pw!='N/A' and ty=='protect' and reqheadersdic['Authorization']!='' and newfileflag==0:
		un1,pw1=codes.parseHeaders("","",reqheadersdic,'auth')
		if pw1!=pw:		
			rv=codes.error_4(403,'confiles/error/403.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv,'403'	
	if un!='N/A' and pw!='N/A' and ty=='proxy' and reqheadersdic['Proxy-Authorization']=='' and newfileflag==0:
		resheadersdic['Proxy-Authenticate']='Basic realm="Access to the protected file", charset="UTF-8"'
		rv=codes.error_4(407,'confiles/error/407.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return rv,'407'
	if un!='N/A' and pw!='N/A' and ty=='proxy' and reqheadersdic['Proxy-Authorization']!='' and newfileflag==0:
		un1,pw1=codes.parseHeaders("","",reqheadersdic,'pauth')
		if pw1!=pw:		
			rv=codes.error_4(403,'confiles/error/403.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return rv,'403'
	if newfileflag==1:
		f=open(filename1,"w+")
		f.write(data)
		f.close()
		mime_type=""
		if(reqheadersdic['Content-Type']==""):
			mime = magic.Magic(mime=True)
			mime_type=mime.from_file(filename1)
		else:
			mime_type=reqheadersdic['Content-Type']
		check_var(filename,reqheadersdic,mime_type,pathdic)
		resheadersdic['Location']=filename
		rv=codes.success_200(201,filename1,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,'',num,cookie_dict,address)
		return rv,'201'
	if newfileflag==0:
		if(reqheadersdic['Content-Range']==""):
			f=open(filename1,"w")
			f.write(data)
			f.close()
		else:
			f=open(filename1,"r+b")
			ranges=reqheadersdic['Content-Range'].split()
			range_av=ranges[1].split("/")
			range_occ=range_av[0].split("-")
			f.seek(int(range_occ[0].strip()),0)
			f.write(data.strip("\r\n"))
			f.close()
		mime_type=""
		if(reqheadersdic['Content-Type']==""):
			mime = magic.Magic(mime=True)
			mime_type=mime.from_file(filename1)
		else:
			mime_type=reqheadersdic['Content-Type']
		check_existing_var(filename,reqheadersdic,mime_type)
		rv=codes.success_200(204,filename1,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,'',num,cookie_dict,address)
		return rv,'204'
		
def handleexpect(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,pathdic,address):
	f_flag=0
	flag=0
	newfileflag=0
	num=0
	try:
		filename,flag=pathreturn(message[1],flag)
		filename1=str(pathdic['docpath'])+'/'+filename
		f=open(filename1)
	except:
		loc,code=compressedclean.checkredirect(filename,pathdic)
		if loc!='N/A' and code!=000:
			rv=codes.error_4(417,'confiles/error/417.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return 417,rv
		newfileflag=1
	if len(message)>3:
		codes.parseHeaders("",headers[1:-2],reqheadersdic,'')
	if ((reqheadersdic['Host']=='' or reqheadersdic['Host']!='localhost:1234') and flag==0):
		rv=codes.error_4(417,'confiles/error/417.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return 417,rv
	if reqheadersdic['Last-Modified']!='' and newfileflag==0:
		dt=os.path.getmtime(filename1)
		date1=str(datetime.datetime.utcfromtimestamp(dt))
		given_date=str(datetime.datetime.strptime(reqheadersdic['Last-Modified'],'%a, %d %b %Y %H:%M:%S GMT'))
		if date1>given_date:
			rv=codes.error_4(417,'confiles/error/417.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return 417,rv
	un,pw,ty=compressedclean.checkprotect(filename,pathdic)
	if un!='N/A' and pw!='N/A' and ty=='protect' and reqheadersdic['Authorization']=='' and newfileflag==0:
		rv=codes.error_4(417,'confiles/error/417.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return 417,rv
	if un!='N/A' and pw!='N/A' and ty=='protect' and reqheadersdic['Authorization']!='' and newfileflag==0:
		un1,pw1=codes.parseHeaders("","",reqheadersdic,'auth')
		#print(pw)
		if pw1!=pw:		
			rv=codes.error_4(417,'confiles/error/417.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return 417,rv	
	if un!='N/A' and pw!='N/A' and ty=='proxy' and reqheadersdic['Proxy-Authorization']=='' and newfileflag==0:
		rv=codes.error_4(417,'confiles/error/417.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return 417,rv
	if un!='N/A' and pw!='N/A' and ty=='proxy' and reqheadersdic['Proxy-Authorization']!='' and newfileflag==0:
		un,pw=codes.parseHeaders("","",reqheadersdic,'pauth')
		if pw!=pw:		
			rv=codes.error_4(417,'confiles/error/417.html',reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
			return 417,rv
	rv='HTTP/1.1 100 Continue\n'
	return 100,rv
		
