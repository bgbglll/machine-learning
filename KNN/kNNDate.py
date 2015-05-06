
from numpy import *
import scipy
import matplotlib
import matplotlib.pyplot as plt
def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines);
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line = line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(listFromLine[-1])
        index+=1
    return returnMat,classLabelVector

datingDataMat,datingLabels=file2matrix('datingTestSet.txt')

fig = plt .figure ()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels)[:],15.0*array(datingLabels)[:])
plt.xlabel("videogame")
plt.ylabel("icecream")
plt.title("percent")
plt.show()

