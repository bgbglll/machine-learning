import re
from time import sleep
from weibo import APIClient
import sys, os, urllib, urllib2 
import json
import jieba
from time import sleep
def textParse(bigString):
    urlsRemoved = re.sub('(http:[/][/]|www.)([a-z]|[A-Z]|[0-9]|[/.]|[~])*', '', bigString)    
    return [urlsRemoved]

def getLotsOfTweets(searchStr):
    APP_KEY = '1204921485' 
    APP_SECRET = '874bbefcc3391b87d17f81707bd2704c' 
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
    return_redirect_uri = f.url  
    code = return_redirect_uri.split('=')[1]  #  
    token = api.request_access_token(code,CALLBACK_URL)
    access_token=token.access_token
    expires_in=token.expires_in
    api.set_access_token(access_token, expires_in)

   # print(api.statuses.public_timeline.get(count=1))
    #statuses=api.statuses.friends_timeline.get(count=50,page=1)['statuses']
    #print(statuses)
    #length = len(statuses)
    #print(length)  
    #输出了部分信息 
    #print(statuses[2]['text'])
    #seg_list = jieba.cut(statuses[2]['text']) 
    #print(seg_list)
    #for seg in seg_list:
    #    print (seg)
    pages=3
    for j in range(1,pages):
        statuses=api.statuses.friends_timeline.get(count=50,page=j)['statuses']
        length = len(statuses)
        sleep(1)
        for i in range(0,length):  
        #print('昵称：'+statuses[i]['user']['screen_name'].encode('gbk', 'ignore')) 
        #print('简介：'+statuses[i]['user']['description'].encode('gbk', 'ignore'))  
        #print('位置：'+statuses[i]['user']['location'].encode('gbk', 'ignore'))
            temp = statuses[i]['text'].encode('gbk', 'ignore')  
            print('微博：'+temp)
            seg_list = jieba.cut(temp) 
            print(seg_list)
            sleep(1)
            for seg in seg_list:
                print(type(seg.encode('gbk', 'ignore')))
                print (seg.encode('gbk', 'ignore'))  
      
    
    
      
    #jsonStr = json.dumps(convertedDict)
    #print ("jsonStr=",jsonStr)
    #print(convertedDict['text'])
    #you can get 1500 results 15 pages * 100 per page
    #resultsPages = []
    #r = api.search.suggestions.users(uid='15926175292')
    #for st in r.statuses:
    #    print(st.text)
    #searchResults = api.GetSearch(searchStr)
    #return resultsPages

getLotsOfTweets('a')
#print(lotsOweibos)
