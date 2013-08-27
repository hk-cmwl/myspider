# -*- coding: gbk -*-
import urllib2
import re

def spider(starturl,urlfilter,localfilter):
    oldq=[]
    newq=[]
    result=[]
    newq.append(starturl)
    count=0
    while newq:#只要newq队列非空
        flag=0
        newurl=newq.pop()#加入list尾部
        for oldurl in oldq:#检查此url是否已经被处理过
            if oldurl == newurl:#此url已经被处理过了
                #print oldurl+'已被处理过！'
                flag=1
                break
        if flag == 0:#此url未被处理过
            if newurl:
                print '正在处理链接：'+newurl
                oldq.append(newurl)#加入被处理队列
                try:
                    context=urllib2.urlopen(newurl,timeout=20).read()#读取该URL对应网页信息
                except:
                    print '无法处理链接：'+newurl
                    continue
                m=re.finditer(urlfilter,context)
                for tmpm in m:
                    if tmpm.group(2):#非空链接
                        if tmpm.group(2)[0] == '.':#新链接第一个字符为.说明是相对路径，要进行相关处理
                            #暂时过滤
                            continue
                        elif tmpm.group(2)[0] == 'h':#新链接的第一个字符为h说明是完整路径，但是域名必须是bistu.edu.cn
                            try:
                                x=re.match(localfilter,tmpm.group(2))#域名过滤
                            except:
                                x=''
                            try:
                                y=re.search('(.*)/(.*)',tmpm.group(2))#提取/后内容
                            except:#如果y没值，那么就给个空数组
                                y=''
                            hzflag=1
                            if y:
                                try:
                                    z=re.search('(.*)\.(.*)',y.group(2))#提取后缀
                                except:
                                    z=''
                                if z:
                                    if z.group(2) <> 'html' and z.group(2) <> 'php' and z.group(2) <> 'htm':#如果有后缀，此为要求匹配后缀
                                        hzflag=0
                            if x and hzflag==1:
                                count=count+1
                                newq.insert(0,tmpm.group(2))#加入list首部
                                try:
                                    print tmpm.group(2)+"  说明：  "+tmpm.group(4).decode('UTF-8').encode('gbk')
                                except:
                                    try:
                                        print tmpm.group(2)+"  说明：  "+tmpm.group(4)
                                    except:
                                        print tmpm.group(2)+"的说明解码失败！"
                            else:
                                continue
                        else:#过滤掉其它形式的链接
                            continue
                    else:#空链接，直接跳过
                        continue
            else:
                continue
    return

urlfilter=re.compile(r'<a(.*?)href="(.*?)"(.*?)>(.*?)</a>')
localfilter=re.compile('http(s?)://(.*?).bistu.edu.cn')
starturl='http://www.bistu.edu.cn/'
spider(starturl,urlfilter,localfilter)
