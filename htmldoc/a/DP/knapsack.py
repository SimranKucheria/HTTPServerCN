def subsetSum(arr,sum1,n,m):
	t=[[ True for i in range(m+1)]for j in range (n+1)]
	for i in range(n+1):
		for j in range(m+1):
			if(i==0 ):
				t[i][j]=False
			if(j==0):
				t[i][j]=True
	for i in range(1,n+1):
		for j in range(1,m+1):
			if(arr[i-1]<=j):
				t[i][j]=t[i-1][j-arr[i-1]] or t[i-1][j]
			else:
				t[i][j]=t[i-1][j]
	print(t[n][m])
arr=[2,7,10]
sum1=11
subsetSum(arr,sum1,3,17)

