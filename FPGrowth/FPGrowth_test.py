import re
from time import sleep
from weibo import APIClient
import sys, os, urllib, urllib2 
import json
import jieba
from time import sleep
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      #needs to be updated
        self.children = {} 
    
    def inc(self, numOccur):
        self.count += numOccur
        
    def disp(self, ind=1):
        print '  '*ind, self.name, ' ', self.count
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet, minSup=1): #create FP-tree from dataset but don't mine
    headerTable = {}
    #go over dataSet twice
    for trans in dataSet:#first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in headerTable.keys():  #remove items not meeting minSup
        if headerTable[k] < minSup: 
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    #print 'freqItemSet: ',freqItemSet
    if len(freqItemSet) == 0: return None, None  #if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link 
    #print 'headerTable: ',headerTable
    retTree = treeNode('Null Set', 1, None) #create tree
    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        localD = {}
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset
    return retTree, headerTable #return tree and header table

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) #incrament count
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table 
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:#call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):   #this version does not use recursion
    while (nodeToTest.nodeLink != None):    #Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    print(retDict)
    return retDict

def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
    
def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]#(sort header table)
    for basePat in bigL:  #start from bottom of header table
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #print 'finalFrequent Item: ',newFreqSet    #append to set
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        #print 'condPattBases :',basePat, condPattBases
        #2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead = createTree(condPattBases, minSup)
       # print 'head from conditional tree: ', myHead
        if myHead != None: #3. mine cond. FP-tree
            #print 'conditional tree for: ',newFreqSet
            #myCondTree.disp(1)            
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def textParse(bigString):
    urlsRemoved = re.sub('(http:[/][/]|www.)([a-z]|[A-Z]|[0-9]|[/.]|[~])*', '', bigString)    
    return urlsRemoved

def getLotsOfWeibos():
    APP_KEY = '3324068306' 
    APP_SECRET = 'df6a69a7115ac6cdb9661068dd60c0c5' 
    CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
    api = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    authorize_url = api.get_authorize_url() 
    #print(authorize_url) 
    #webbrowser.open_new(authorize_url)
    params = urllib.urlencode({ 'action':'submit', 'withOfficalFlag':'0', 'ticket':'', 'isLoginSina':'',  'response_type':'code', 'regCallback':'', 'redirect_uri':CALLBACK_URL, 'client_id':APP_KEY, 'state':'', 'from':'', 'userId':'15926175292', 'passwd':'lbg8230889', })  
    login_url = 'https://api.weibo.com/oauth2/authorize' 
    #response = urllib2.urlopen(authorize_url) 
    headers = { 'Referer' : authorize_url } 
    request = urllib2.Request(login_url, params, headers)  
    opener = urllib2.build_opener(); 
    urllib2.install_opener(opener)  
    f = opener.open(request)  
    #print(f)
    return_redirect_uri = f.url  
    code = return_redirect_uri.split('=')[1]  #  
    token = api.request_access_token(code,CALLBACK_URL)
    access_token=token.access_token
    expires_in=token.expires_in
    api.set_access_token(access_token, expires_in)   
    resultPages=[]
    pages=1
    dataSeta=['iG 3:1 zhansheng VG��gongxi iG��http:///www.aa.com','iG 3:1 zhansheng VG��http:///www.aa.com',' iG zhansheng VG haha��http:///www.aa.com','iG zhansheng VG��ha http:///www.aa.com']
    for j in range(1,pages+1):
        #statuses=api.statuses.user_timeline.get(count=1,page=j)['statuses']
        #length = len(statuses)
        #sleep(1)
        #for i in range(0,length):
        #for i in range(0,1):
        
        for temp in dataSeta:         
            #temp = statuses[i]['text'].encode('gbk', 'ignore') 
            #temp = 'iG 3:1սʤVG����ϲiG��http:///www.aa.com'
            #print('΢����'+temp)
            temp = textParse(temp)
            #print(temp)
            seg_list = jieba.cut(temp) 
            #print(seg_list)
            #sleep(1)
            tempPages=[]
            for seg in seg_list:
                #print (seg.encode('gbk', 'ignore'))
                if(len(seg)>=2):  
                    tempPages.append(seg.encode('gbk', 'ignore'))
            resultPages.append(tempPages)
            print(resultPages)
    return resultPages

def mineWeibos(WeiboArr, minSup=5):
    print(WeiboArr)
    initSet = createInitSet(WeiboArr)
    
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    myFPtree.disp()
    myFreqList = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), myFreqList)
    return myFreqList


listOfTerms = mineWeibos(getLotsOfWeibos(),4)
#print(len(listOfTerms))
for t in listOfTerms:
    print('FPset(['),
    i=1;
    length = len(t)
    for tt in t:
        #sleep(1) 
        print(tt),
        if(i<length):
            print(','),
        i=i+1
    print('])')

#resultPages=getLotsOfWeibos()
#for i in resultPages:
#    print(i)


#simpDat = loadSimpDat()
#print(simpDat)
#initSet=createInitSet(simpDat)
#print(initSet)
#myFPtree,myHeaderTab = createTree(initSet,3)
#myFPtree.disp()
#print(findPrefixPath('x',myHeaderTab['x'][1]))
#freqItems=[]
#mineTree(myFPtree,myHeaderTab,3,set([]),freqItems)
#print(freqItems)