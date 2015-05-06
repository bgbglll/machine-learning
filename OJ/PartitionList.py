def partition(self, head, x):
    c=[];d=[]
    #if head == []:
        #return head
    for i in head:
        #print(i)
        if i<x:
            c.append(i)
        else:
            d.append(i)
    c.extend(d)
    return c

#print(partition(0, {}, 0))