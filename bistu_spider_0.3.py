# -*- coding: gbk -*-
import urllib2
import re
def spider(starturl,starturldescription,urlfilter,titlefilter,localfilter):
    olddict={}
    newdict={}
    result={}
    newdict[starturl]=starturldescription
    while newdict:
        kvpair=newdict.popitem()#取出字典的第一个K,V对
        key=kvpair[0]
        value=kvpair[1]
        try:
            x=olddict.get(key)
        except:
            x=''
        if not x:#此url未被处理过
            #读取网页
            olddict[key]='*'
            try:
                context=urllib2.urlopen(key,timeout=20).read()
            except:
                print '无法处理链接：'+key
                continue
            #取得title标签值
            try:
                title=re.search(titlefilter,context).group(2).decode('UTF-8').encode('gbk')
            except:
                try:
                    title=re.search(titlefilter,context).group(2)
                except:
                    title=''

            print '正在处理链接：'+key+'   网页简要说明：'+value+'  网页标题：'+title
            result[key]=value+':::'+title
            
            #下面处理本页面里的所有其它链接
            m=re.finditer(urlfilter,context)
            for tmp in m:
                if not tmp.group(2):#url为空时过滤掉
                    continue
                elif tmp.group(2)[0]=='.':
                    #暂时过滤
                    continue
                elif tmp.group(2)[0]=='h':
                    try:
                        x=re.match(localfilter,tmp.group(2))#域名过滤
                    except:
                        x=''
                    try:
                        y=re.search('(.*)/(.*)',x.group(3))#提取链接最后一个/后的内容
                    except:
                        y=''
                    hzflag=1#后缀标志
                    if y:
                        try:
                            z=re.search('(.*)\.(.*)',y.group(2))#提取后缀
                        except:
                            z=''
                        if z:
                            if z.group(2) <> 'html' and z.group(2) <> 'php' and z.group(2) <> 'htm':#过滤其它形式的后缀如.doc、.rar等
                                    hzflag=0
                    if x and hzflag==1:#满足过滤条件
                        try:
                            valuestr=tmp.group(4).decode('UTF-8').encode('gbk')
                        except:
                            try:
                                valuestr=tmp.group(4)
                            except:
                                valuestr=''
                        if valuestr:
                            newdict[tmp.group(2)]=valuestr
                    else:#不满足过滤条件
                        continue
                else:#不处理其它形式的链接
                    continue
    return result

titlefilter=re.compile(r'<title(.*?)>(.*?)</title>')
urlfilter=re.compile(r'<a(.*?)href="(.*?)"(.*?)>(.*?)</a>')
localfilter=re.compile('http(s?)://(.*?).bistu.edu.cn(.*)')
starturl='http://www.bistu.edu.cn/'
spider(starturl,'北京信息科技大学',urlfilter,titlefilter,localfilter)         
