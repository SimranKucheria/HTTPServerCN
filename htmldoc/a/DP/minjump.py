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

arr=[2,3,1,1,4]
print(reqJumps(arr,5,0))
