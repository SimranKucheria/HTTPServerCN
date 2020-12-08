import math
import sys
def wordbreak(s,width):
	c=[[-1 for i in range(len(s))]for j in range(len(s))]
	for i in range(len(s)):
		c[i][i]=(width-len(s[i]))
		for j in range(i+1,len(s)):
			if(c[i][j-1]-(len(s[j])+1)>=0):
				c[i][j]=c[i][j-1]-(len(s[j])+1)
			
	for i in range(len(s)):
		for j in range(len(s)):
			if(c[i][j]>=0):
				c[i][j]=int(math.pow(c[i][j],2))
			else:
				c[i][j]=sys.maxsize
	minCost=[0 for i in range(len(s))]
	result=[0  for i in range(len(s))]
	for i in range(len(s)-1,-1,-1):
		minCost[i]=c[i][len(s)-1]
		result[i]=len(s)
		for j in range(len(s)-1,i,-1):
			if(c[i][j-1]==sys.maxsize):
				continue
			if(minCost[j]+c[i][j-1]<minCost[i]):
				minCost[i]=minCost[j]+c[i][j-1]
				result[i]=j
	return(minCost[0])		

s=["Tushar","Roy","likes","to","code"]
print(str(wordbreak(s,10))+" is the most optimised representation ")

			
			
			
		
		
