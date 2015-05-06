def removeDuplicates(self, A):
    index=0
    for i in range(1,len(A)):
        if A[index]!=A[i]:
            index=index+1
            A[index]=A[i]
    return index+1

print(removeDuplicates(0,[1,1,2]))