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
	
def delete_file(filename,reqheadersdic,pathdic):
	new_filename=pathdic['docpath']+'/'+filename
	#print(filename)
	name=filename.split('.',1)
	var_name="confiles/varfile/"+name[0]+".var"
	f=open(var_name,"r")
	files=f.readlines()
	#print(files)
	del_f=0
	new_files=[]
	if(reqheadersdic['Content-Encoding']==""):
		reqheadersdic['Content-Encoding']="identity"
	if(reqheadersdic['Content-Language']==""):
		reqheadersdic['Content-Language']="en"
	if(reqheadersdic['Content-Type'][0:6]=="image/"):
		reqheadersdic['Content-Language']="i"
		new=reqheadersdic['Content-Type']+";charset=i"
		reqheadersdic['Content-Type']=new
	for i in files:
		title=i.split(";")
		#print(title)
		if(filename==title[1].strip("\n")):
			encoding=title[0].split(":")
			#print(encoding)
			if(reqheadersdic['Content-Encoding']==encoding[0]):
				#print("inside")
				if(reqheadersdic['Content-Type']!=""):
					if(";" in reqheadersdic['Content-Type']):
						sets=reqheadersdic['Content-Type'].split(";")
						reqheadersdic['Content-Type']=sets[0]
						set_char=sets[1].split("=")
						charset=set_char[1]
					else:
						charset="iso-8859-5"
					if(reqheadersdic['Content-Type']==encoding[1]):
							if(reqheadersdic['Content-Language']==encoding[2]):	
								if(charset==encoding[3]):
									del_f=1
									continue
				else:
					charset="iso-8859-5"
					if(reqheadersdic['Content-Language']==encoding[2]):
								if(charset==encoding[3]):
									del_f=1
									continue
		new_files.append(i)
	if(del_f==1):
		if(len(files)==1):
				cwd=os.getcwd()
				new_var=cwd+'/'+var_name
				os.remove(new_var)
				os.remove(new_filename)
				return 1
		
		os.remove(new_filename)
		if(len(files)==2 and len(new_files)==1):
			f=open(pathdic['verpath'],"r+")
			new_ver=[]
			lists=f.readlines()
			#print(lists)
			for i in lists:
				names=i.split(".",1)
				if(names[0]==name[0]):
					continue
				new_ver.append(i)
			#print(new_ver)
			f=open(pathdic['verpath'],"w+")
			f.writelines(new_ver)
		file1 = open(var_name, 'w') 
		file1.writelines(new_files) 
		return 1
	return 0
def handledelete(message,headers,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num,pathdic,cookie_dict,address):
	f_flag=0
	flag=0
	try:
		filename,flag=pathreturn(message[1],flag)	
		filename1=str(pathdic['docpath'])+'/'+filename
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
		
	suc_code=delete_file(filename,reqheadersdic,pathdic)
	if(suc_code==1):
		rv=codes.success_200(204,filename1,reqheadersdic,resheadersdic,entheadersdic,genheadersdic,'',num,cookie_dict,address)
		return rv,'204'
	else:
		rv=codes.error_4(404,"confiles/error/404.html",reqheadersdic,resheadersdic,entheadersdic,genheadersdic,num)
		return rv,'404'
	#print(reqheadersdic)
