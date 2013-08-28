# -*- coding: utf-8 -*-
import urllib2
import re
import chardet
from urlparse import urljoin
fp=open('test.txt','w')
def spider(starturl,starturldescription,urlfilter,titlefilter,scriptfilter,stylefilter,nbspfilter,localfilter):
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
            olddict[key]=' '
            try:
                context=urllib2.urlopen(key,timeout=20).read()
                chardit=chardet.detect(context)
                context=context.decode(chardit['encoding']).encode('utf-8')
                context=context.replace('\n',' ')
                context=context.replace('\r',' ')
            except:
                print u'无法处理链接：'+key
                continue
            #取得title标签值
            try:
                title=re.search(titlefilter,context).group(2)
            except:
                title=''
            #提取除<script>标签的网页的所有非标签内容
            #过滤<style>标签
            tmpresult0=''
            tmpct0=context
            while tmpct0:
                try:
                    x0=re.match(stylefilter,tmpct0)
                    tmpresult0=tmpresult0+x0.group(1)
                    tmpct0=x0.group(4)
                except:
                    tmpresult0=tmpresult0+tmpct0
                    break
            #过滤<script>标签
            tmpresult1=''
            tmpct1=tmpresult0
            while tmpct1:
                try:
                    x1=re.match(scriptfilter,tmpct1)
                    tmpresult1=tmpresult1+x1.group(1)
                    tmpct1=x1.group(4)
                except:
                    tmpresult1=tmpresult1+tmpct1
                    break
            #过滤&nbsp内容
            tmpresult2=''
            tmpct2=tmpresult1
            while tmpct2:
                try:
                    x2=re.search(nbspfilter,tmpct2)
                    tmpresult2=tmpresult2+x2.group(1)
                    tmpct2=x2.group(2)
                except:
                    tmpresult2=tmpresult2+tmpct2
                    break
            #提取内容
            onlyct=''
            tmp=tmpresult2
            while tmp:
                try:
                    t1=re.match(r'(.*?)<(.*?)>(.*)',tmp)
                    tmp=t1.group(3)
                except:
                    break
                try:
                    ct1=t1.group(1)
                except:
                    ct1=''
                if ct1:
                    onlyct=onlyct+' '+ct1
            print '..........'+key+'..........'+value+'..........'+title+'..........'+onlyct
            result[key]=value+':::'+title+':::'+onlyct
            fp.write(key+':::'+result[key])
            fp.write('\n')
            #下面处理本页面里的所有其它链接
            m=re.finditer(urlfilter,context)
            for tmp in m:
                if not tmp.group(2):#url为空时过滤掉
                    continue
                elif tmp.group(2)[0]=='.':
                    newkey=urljoin(key,tmp.group(2))#URL拼接
                    try:
                        x1=re.match(localfilter,newkey)#域名过滤
                    except:
                        x1=''
                    try:
                        y=re.search('(.*)/(.*)',x1.group(3))#提取链接最后一个/后的内容
                    except:
                        y=''
                    hzflag=1#后缀标志
                    if y:
                        try:
                            z=re.search('(.*)\.(.*)',y.group(2))#提取后缀
                        except:
                            z=''
                        if z:
                            if z.group(2) <> 'html' and z.group(2) <> 'php' and z.group(2) <> 'htm':#过滤其它形式的后缀如.docx、.rar等
                                    hzflag=0
                    if x1 and hzflag==1:#满足过滤条件
                        try:
                            tmpvaluestr=re.match('(.*?)<img(.*?)>(.*)',tmp.group(4))
                            if tmpvaluestr:
                                valuestr='图片链接'
                            else:
                                valuestr=tmp.group(4)
                        except:
                            valuestr=''
                        if not newdict.get(newkey):#不存在才加入
                            newdict[newkey]=valuestr
                    else:#不满足过滤条件
                        continue
                elif tmp.group(2)[0]=='h':
                    try:
                        x1=re.match(localfilter,tmp.group(2))#域名过滤
                    except:
                        x1=''
                    try:
                        y=re.search('(.*)/(.*)',x1.group(3))#提取链接最后一个/后的内容
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
                    if x1 and hzflag==1:#满足过滤条件
                        try:
                            valuestr=tmp.group(4)
                        except:
                            valuestr=''
                        if not newdict.get(tmp.group(2)):
                            newdict[tmp.group(2)]=valuestr
                    else:#不满足过滤条件
                        continue
                else:#不处理其它形式的链接
                    continue
    return result
nbspfilter=re.compile(r'(.*?)&nbsp;(.*)')
stylefilter=re.compile(r'(.*?)<style(.*?)>(.*?)</style>(.*)',re.I)
scriptfilter=re.compile(r'(.*?)<script(.*?)>(.*?)</script>(.*)',re.I)
titlefilter=re.compile(r'<title(.*?)>(.*?)</title>',re.I)
urlfilter=re.compile(r'<a(.*?)href="(.*?)"(.*?)>(.*?)</a>',re.I)
localfilter=re.compile('http(s?)://(.*?).bistu.edu.cn(.*)',re.I)
starturl='http://www.bistu.edu.cn/'
result=spider(starturl,'bistu',urlfilter,titlefilter,scriptfilter,stylefilter,nbspfilter,localfilter)         

#for r in result:
    #fp.write(r)
    #fp.write('\n')
fp.close()
