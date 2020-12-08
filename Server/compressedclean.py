import string
import hashlib
def getvals(line):
	line=line.split(';')
	fn=line[1]
	e,p,l,ch=line[0].split(':')
	return e,p,l,ch,fn

def getline(filename):
	nf=filename.split('.',1)
	f=''
	f1=open('confiles/varfile/'+nf[0]+'.var')
	for x in f1:
		f+=str(x)
	f=f.split('\n')
	for i in range (len(f)):
		if f[i]=='':
			break
	f=f[0:i]
	return f

def delval(d):
	delist=[]				
	for m in d:
		if d[m]==0.0 or d[m]==-2.0:
			delist.append(m)
	for m in delist:
		del d[m]

def getiterarr(mm):
	m=[]
	m1=[]
	if mm=={}:
		m1=[1]
	else:
		delval(mm)
		if mm!={}:
			m=sorted(mm.items(), key=lambda x: x[::-1], reverse=True)
			i=0
			for i in m:
				i=str(i[0]).split()
				m1.append(i[0])
		else:
			m1=[0]
	return m1
def getarr(enco,priority,langs,chars):
	en1=getiterarr(enco)
	pri1=getiterarr(priority)
	la1=getiterarr(langs)
	cha1=getiterarr(chars)
	if 'identity' in en1:
		qv=enco['identity']
		for it in enco:
			if enco[it]==qv and it!='identity':
				a=en1.index('identity')
				b=en1.index(it)
				if a>b:
					en1[a],en1[b]=en1[b],en1[a]
	return en1,pri1,la1,cha1
def getrvals(line):
	line=line.split(';')
	fn=line[0]
	rfn=line[1]
	code=line[2]
	return fn,rfn,code
def getpvals(line):
	line=line.split(';')
	fn=line[0]
	un=line[1]
	pw=line[2]
	ty=line[3]
	return fn,un,pw,ty
def checkprotect(fn,pathdic):
	f=''
	f1=open(pathdic['plpath'])
	for x in f1:
		f+=str(x)
	f=f.split('\n')
	for i in range (len(f)):
		if f[i]=='':
			break
	f=f[0:i]
	for rcmb in f:
		filename,un,pw,ty=getpvals(rcmb)
		if filename==fn:
			return un,pw,ty
	else:
		return 'N/A','N/A','N/A'
def checkredirect(fn,pathdic):
	f=''
	f1=open(pathdic['rlpath'])
	for x in f1:
		f+=str(x)
	f=f.split('\n')
	for i in range (len(f)):
		if f[i]=='':
			break
	f=f[0:i]
	for rcmb in f:
		filename,rfn,code=getrvals(rcmb)
		if filename==fn:
			return rfn,int(code)
	else:
		return 'N/A',000

def addmd5(fn,ent):
	with open(fn, "rb") as f:
		file_hash = hashlib.md5()
    		chunk = f.read(8192)
    		while chunk:
        		file_hash.update(chunk)
       			chunk = f.read(8192) 
	CMD5 = file_hash.hexdigest().decode('hex').encode('base64')
	ent['Content-MD5']=CMD5
def contentnego(filename,req,res,ent,enco,priority,langs,chars):
	afn=filename
	f=getline(filename)
	#print enco,priority,langs,chars
	if enco==priority==langs==chars=={}:
		for cmb in f:
			e,p,l,ch,fn=getvals(cmb)
			if fn==afn:
				if ch!='i':								
					ent['Content-Type']=p+'; charset='+ch
				else:
					ent['Content-Type']=p
				ent['Content-Encoding']=e
				if l!='i':
					ent['Content-Language']=l
				return filename
	else:	
		en1,pri1,la1,cha1=getarr(enco,priority,langs,chars)
		if en1==[0] or pri1==[0] or la1==[0] or cha1==[0]:
			return 'N/A'
		fl=0
		check=2
		for a in en1:
			for b in pri1:
				y=b
				if y!='*/*' and y!=1:
					y=y.split('/')
					if y[1]=='*':
						check=len(y[0])
						fl=1
				for c in la1:
					for d in cha1:
						for cmb in f:
							e,p,l,ch,fn=getvals(cmb)
							if (e==a or enco=={} or e=='i') and (p==b or priority=={} or p=='i' or b=='*/*'  or (fl==1 and p[0:check-1]==b[0:check-1])) and (l==c or langs=={} or l=='i' or c=="*") and (ch==d or chars=={} or ch=='i' or d=='*' ):
									if ch!='i':					
										ent['Content-Type']=p+'; charset='+ch
									else:
										ent['Content-Type']=p
									ent['Content-Encoding']=e
									if l!='i':
										ent['Content-Language']=l
									return fn
									
			fl=0
		return 'N/A'

