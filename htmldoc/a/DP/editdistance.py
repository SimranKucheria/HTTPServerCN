def editdistance(str1,str2,m,n):
	t=[[0 for i in range(n+1)]for j in range(m+1)]
	
	for i in range(m+1):
		for j in range(n+1):
			if(i==0):
				t[i][j]= j
			elif(j==0):
				t[i][j]=i
			elif(str1[i-1]==str2[j-1]):
				t[i][j]=t[i-1][j-1]
			else:
				t[i][j]=(1+ min(t[i][j-1],t[i-1][j-1],t[i-1][j]))
	return t[m][n]
	
str1="sunday"
str2="saturday"
print(editdistance(str1,str2,len(str1),len(str2)))
	
