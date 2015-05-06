from math import log
import operator
import treePlotter
def calcShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 1
        else:
            labelCounts[currentLabel] +=1
    shannonEnt=0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

def createDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels=['no surfacing','flippers']
    return dataSet,labels

def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in  dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            #print(featVec[:axis])
            reducedFeatVec.extend(featVec[axis+1:])
            #print(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain>bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
        return bestFeature

def majorityCnt(ClassList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1;
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=true)
    return calssCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    #print(classList)
    #print(classList.count(classList[0]))
    if classList.count(classList[0]) == len(classList):
       # print(len(classList))
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

def classify(inputTree,featLables,testVec):
    firstStr = list(inputTree.keys())[0]
    #print(firstStr)
    secondDict = inputTree[firstStr]
    featIndex = featLables.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] ==key :
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key],featLables,testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'wb')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)

fr = open('lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
print(lenses)
lensesLabels = ['tearRate','astigmatic','age','prescript']
lensesTree = createTree(lenses,lensesLabels)
print(lensesTree)
treePlotter.createPlot(lensesTree)
#myDat,labels=createDataSet()
#myTree=treePlotter.retrieveTree(0)
#storeTree(myTree,'classifierStorage.txt')
#print(grabTree('classifierStorage.txt'))
#print(labels)
#print(myTree)
#print(classify(myTree,labels,[1,0]))
#print(classify(myTree,labels,[1,1]))
#print(chooseBestFeatureToSplit(myDat))
#print(myDat)
#print(calcShannonEnt(myDat))
#print(splitDataSet(myDat,0,1))
#print(createTree(myDat,labels))