import jieba  
import re

def textParse(bigString):
    urlsRemoved = re.sub('(http:[/][/]|www.)([a-z]|[A-Z]|[0-9]|[/.]|[~])*', '', bigString)
    print(urlsRemoved)    
    return urlsRemoved
bigString = '我来到北京清华大学,http://aa.com'
print(textParse(bigString))  
seg_list = jieba.cut(textParse(bigString),cut_all=True) 
resultPages=[]
for seg in seg_list:
                print (seg)  
                resultPages.append([seg.encode('gbk', 'ignore')])
print(resultPages)
for i in resultPages:
    for j in i:
        gbk_string=j
        print(gbk_string)
        print(type(gbk_string))
