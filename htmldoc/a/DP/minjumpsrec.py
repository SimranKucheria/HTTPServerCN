import sys
def reqJumps(arr,n,currPos):
	if(currPos>=n-1):
		return 0
	maxSteps=arr[currPos]
	minJump=sys.maxsize
	while(maxSteps>0):
		minJump=min(minJump,1+reqJumps(arr,n,currPos+maxSteps))
		maxSteps=maxSteps-1
	return minJump

arr=[1, 3, 5, 8, 9, 2, 6, 7, 6, 8, 9]
print(reqJumps(arr,11,0))
