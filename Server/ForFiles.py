import glob
import os
import magic
import langid

filelist=[]
rootpath=''
verfilelist=[]
verrootpath=''

def checkfolder(filename):
	check = os.path.isdir(filename)
     	return check

def delverfiles(path):
	global verrootpath,verfilelist
	for filename in glob.iglob(path + '**/**'):
		m=checkfolder(filename)
		if m==True:
			delverfiles(filename)
			os.rmdir(filename)
		if m==False:
			os.remove(filename)
	     		#print filename
     	return
def allfiles(path):
	global rootpath,filelist
	for filename in glob.iglob(path + '**/**'):
		m=checkfolder(filename)
		if m==True:
			allfiles(filename)
		if m==False:
			filename=filename.replace(rootpath,'')
     			filelist.append(filename)
     			#print filename
     	return
     	
def allverfiles(path):
	global verrootpath,verfilelist
	for filename in glob.iglob(path + '**/**'):
		m=checkfolder(filename)
		if m==True:
			allverfiles(filename)
		if m==False:
			filename=filename.replace(verrootpath,'')
	     		verfilelist.append(filename)
	     		#print filename
     	return

def enco(af):
	j=af
	j=j.split('/')
	j=j[-1]
	j=j.split('.')
	j=j[-1]
	string=''
	if j=='gz':
		string+='gzip:'
	elif j=='lzw':
		string+='compress:'
	elif j=='zlib':
		string+='deflate'
	else:
		string+='identity:'
	return string

def lang(af):
	global rootpath
	f=open(rootpath+af,'r+')
	x=f.read()
	f.close()
	return langid.classify(x)[0]+':'
		

def towrite(j):
	global rootpath
	string=''
	m=rootpath
	flag=0
	m+=j
	string+=enco(j)
	f1=open(m,'a+')
	mime = magic.Magic(mime=True)
	mime_type=mime.from_file(m)
	string+=mime_type+":"
	nlist=['image','gzip','deflate','compress']
	for i in nlist:
		if i in string:
			string+='i:'
			flag=1
			break
	if flag==0:
		string+=lang(j)
	string+='i;'+j[1:]+'\n'
	return string
	

def checkveradded(af,vf):
	global verrootpath
	namelist=[]
	m=verrootpath+'/'
	m+=vf
	f2=open(m,'r+')
	charac=f2.readlines()
	new_list=[]
	for i in charac:
		line=i.split(";")
		if(len(line)>=2):
			namelist.append(line[1].strip("\n"))
	f2.close()
	name=af[1:]
	if name not in namelist:
		string=towrite(af)
		f2=open(m,'a+')
		f2.write(string)
		f2.close()

def createdic(vf,dic):
	global verrootpath
	f=open(verrootpath+'/'+vf,'r+')
	d=f.read()
	d=d.splitlines()
	k=vf[1:]
	dic[k]=[]
	for i in d:
		i.strip()
		i=i.split(';')
		if len(i)>=2:
			dic[k].append(i[1])
			
def remsome(dic,a):
	global verrootpath
	m=dic[a]
	#print m
	with open(verrootpath+'/'+a, "r+") as f:
    		d = f.readlines()
    		f.seek(0)
    		#print d
    		for i in d:
    			v=i.split(';')
    			#print v
        		if len(v)>=2 and v[1][:-1] not in m:
            			f.write(i)
    		f.truncate()
    		f.close()
    	if os.path.getsize(verrootpath+'/'+a)==0:
    		os.remove(verrootpath+'/'+a)
    	dic[a]={}
    	
	
def delold():
	global verrootpath,verfilelist,filelist
	vf=verfilelist
	dic={}
	for j in verfilelist:
		createdic(j,dic)
	for j in filelist:
		for m in dic:
			while j[1:] in dic[m]:
					dic[m].remove(j[1:])
	#print dic
	for g in dic:
		if dic[g]!=[]:
	#		print "DELETING NOW"
			remsome(dic,g)
	
	#print "NOTHING TO DELETE"
	return
						
def addnew():
	global verrootpath,verfilelist,filelist
	for j in filelist:
		k=j
		k=k.split('/')
		ia=k[:-1]
		ia=('/').join(ia)
		k=k[-1]
		k=k.split('.')
		i=k[0]
		i=ia+'/'+i+'.var'
		#print i,verrootpath
		if i not in verfilelist:
			fn=verrootpath+i
			if not os.path.exists(os.path.dirname(fn)):
    				try:
        				os.makedirs(os.path.dirname(fn))
    				except OSError as exc: # Guard against race condition
        				if exc.errno != errno.EEXIST:
         					raise
			f=open(fn,'a+')
			string=towrite(j)
			f.write(string)
			f.close()
			
			if i[0]=='/':
				i=i[1:]
			verfilelist.append('/'+i)
			
		elif i in verfilelist:
			checkveradded(j,i)

	#FOR THE VERSION.TXT
		#fn=verrootpath+'/'+i
		#f=open(fn,'r+')
		#charac=f.read()
		#charac=charac.splitlines()
		#n=0
		#for f1 in charac:
		#	if f1!='':
		#		n+=1
		#f.close()
		#print n,charac
		#if n>=2:
		#	vfn=open(version,'r+')
		#	names=vfn.read()
		#	names=names.splitlines()
		#	vfn.close()
		#	k=j
		#	if k[1:] not in names:
		#		vfn=open(version,'a+')
		#		vfn.write(k[1:]+'\n')
		#		vfn.close()	
	return
	
def new(pathdic):
	documents=pathdic['docpath']
	#versionfile=pathdic['verpath']
	varfiles="confiles/varfile"
	global rootpath,verrootpath,filelist,verfilelist
	rootpath=documents
	verrootpath=varfiles
	delverfiles(varfiles)
	#return
	allfiles(documents)
	allverfiles(varfiles)
	#print filelist
	#print
	#print verfilelist
	#print
	addnew()
	delold()
	
	return
