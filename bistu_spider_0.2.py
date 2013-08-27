# -*- coding: gbk -*-
import urllib2
import re

def spider(starturl,urlfilter,localfilter):
    oldq=[]
    newq=[]
    result=[]
    newq.append(starturl+":::"+"起始爬虫页")
    count=0
    while newq:#只要newq队列非空
        flag=0
        newcombine=newq.pop()#加入list尾部，从这儿弹出来的所有链接都是有:::分隔的
        newurl=newcombine.split(":::")[0]
        newsign=newcombine.split(":::")[1]
        for oldurl in oldq:#过滤掉已处理过的链接
            if oldurl == newurl:
                flag=1
                break
        if flag == 0:#此url未被处理过
            oldq.append(newurl)#加入被处理队列
            try:
                context=urllib2.urlopen(newurl,timeout=20).read()#读取该URL对应网页信息
            except:
                print '无法处理链接：'+newurl
                continue
            print '正在处理链接：'+newurl+'    网页说明：'+newsign
            result.append(newcombine)#到此的链接都是可处理的，用一个列表保存起来
            m=re.finditer(urlfilter,context)#根据urlfilter返回一个迭代器
            for tmpm in m:#处理当前网页的其它链接
                if tmpm.group(2):#过滤掉空链接
                    if tmpm.group(2)[0] == '.':#新链接第一个字符为.说明是相对路径，要进行相关处理
                        #暂时过滤
                        continue
                    elif tmpm.group(2)[0] == 'h':#新链接的第一个字符为h说明是完整路径
                        try:
                            x=re.match(localfilter,tmpm.group(2))#域名过滤，域名必须是bistu.edu.cn，防止爬取太多外网内容
                        except:
                            x=''
                        try:
                            y=re.search('(.*)/(.*)',x.group(3))#提取链接最后一个/后的内容，可能为空，即什么都没有，此处不用tmpm.group(2)，因为可能存在http://www.bistu.edu.cn的情况
                        except:#如果y没值，那么就给个空数组
                            y=''
                        hzflag=1
                        if y:
                            try:
                                z=re.search('(.*)\.(.*)',y.group(2))#提取后缀
                            except:
                                z=''
                            if z:
                                if z.group(2) <> 'html' and z.group(2) <> 'php' and z.group(2) <> 'htm':#过滤其它形式的后缀如.doc、.rar等
                                    hzflag=0
                        if x and hzflag==1:
                            #先解码，后插入
                            try:
                                insertstr=tmpm.group(2)+":::"+tmpm.group(4).decode('UTF-8').encode('gbk')
                            except:
                                try:
                                    insertstr=tmpm.group(2)+":::"+tmpm.group(4)
                                except:
                                    insertstr=''
                                    #print tmpm.group(2)+"的说明解码失败！"
                            if insertstr:
                                newq.insert(0,insertstr)#加入list首部
                                count=count+1#计数加1
                        else:
                            continue
                    else:#过滤掉其它形式的链接
                        continue
                else:#空链接，直接跳过，处理该页面下一个链接
                    continue
    return

urlfilter=re.compile(r'<a(.*?)href="(.*?)"(.*?)>(.*?)</a>')
localfilter=re.compile('http(s?)://(.*?).bistu.edu.cn(.*)')
starturl='http://www.bistu.edu.cn/'
spider(starturl,urlfilter,localfilter)
