# -*- coding: gbk -*-
import urllib2
import re
def spider(starturl,starturldescription,urlfilter,titlefilter,localfilter):
    olddict={}
    newdict={}
    result={}
    newdict[starturl]=starturldescription
    while newdict:
        kvpair=newdict.popitem()#ȡ���ֵ�ĵ�һ��K,V��
        key=kvpair[0]
        value=kvpair[1]
        try:
            x=olddict.get(key)
        except:
            x=''
        if not x:#��urlδ�������
            #��ȡ��ҳ
            olddict[key]='*'
            try:
                context=urllib2.urlopen(key,timeout=20).read()
            except:
                print '�޷��������ӣ�'+key
                continue
            #ȡ��title��ǩֵ
            try:
                title=re.search(titlefilter,context).group(2).decode('UTF-8').encode('gbk')
            except:
                try:
                    title=re.search(titlefilter,context).group(2)
                except:
                    title=''

            print '���ڴ������ӣ�'+key+'   ��ҳ��Ҫ˵����'+value+'  ��ҳ���⣺'+title
            result[key]=value+':::'+title
            
            #���洦��ҳ�����������������
            m=re.finditer(urlfilter,context)
            for tmp in m:
                if not tmp.group(2):#urlΪ��ʱ���˵�
                    continue
                elif tmp.group(2)[0]=='.':
                    #��ʱ����
                    continue
                elif tmp.group(2)[0]=='h':
                    try:
                        x=re.match(localfilter,tmp.group(2))#��������
                    except:
                        x=''
                    try:
                        y=re.search('(.*)/(.*)',x.group(3))#��ȡ�������һ��/�������
                    except:
                        y=''
                    hzflag=1#��׺��־
                    if y:
                        try:
                            z=re.search('(.*)\.(.*)',y.group(2))#��ȡ��׺
                        except:
                            z=''
                        if z:
                            if z.group(2) <> 'html' and z.group(2) <> 'php' and z.group(2) <> 'htm':#����������ʽ�ĺ�׺��.doc��.rar��
                                    hzflag=0
                    if x and hzflag==1:#�����������
                        try:
                            valuestr=tmp.group(4).decode('UTF-8').encode('gbk')
                        except:
                            try:
                                valuestr=tmp.group(4)
                            except:
                                valuestr=''
                        if valuestr:
                            newdict[tmp.group(2)]=valuestr
                    else:#�������������
                        continue
                else:#������������ʽ������
                    continue
    return result

titlefilter=re.compile(r'<title(.*?)>(.*?)</title>')
urlfilter=re.compile(r'<a(.*?)href="(.*?)"(.*?)>(.*?)</a>')
localfilter=re.compile('http(s?)://(.*?).bistu.edu.cn(.*)')
starturl='http://www.bistu.edu.cn/'
spider(starturl,'������Ϣ�Ƽ���ѧ',urlfilter,titlefilter,localfilter)         
