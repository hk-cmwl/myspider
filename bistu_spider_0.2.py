# -*- coding: gbk -*-
import urllib2
import re

def spider(starturl,urlfilter,localfilter):
    oldq=[]
    newq=[]
    result=[]
    newq.append(starturl+":::"+"��ʼ����ҳ")
    count=0
    while newq:#ֻҪnewq���зǿ�
        flag=0
        newcombine=newq.pop()#����listβ������������������������Ӷ�����:::�ָ���
        newurl=newcombine.split(":::")[0]
        newsign=newcombine.split(":::")[1]
        for oldurl in oldq:#���˵��Ѵ����������
            if oldurl == newurl:
                flag=1
                break
        if flag == 0:#��urlδ�������
            oldq.append(newurl)#���뱻�������
            try:
                context=urllib2.urlopen(newurl,timeout=20).read()#��ȡ��URL��Ӧ��ҳ��Ϣ
            except:
                print '�޷��������ӣ�'+newurl
                continue
            print '���ڴ������ӣ�'+newurl+'    ��ҳ˵����'+newsign
            result.append(newcombine)#���˵����Ӷ��ǿɴ���ģ���һ���б�������
            m=re.finditer(urlfilter,context)#����urlfilter����һ��������
            for tmpm in m:#����ǰ��ҳ����������
                if tmpm.group(2):#���˵�������
                    if tmpm.group(2)[0] == '.':#�����ӵ�һ���ַ�Ϊ.˵�������·����Ҫ������ش���
                        #��ʱ����
                        continue
                    elif tmpm.group(2)[0] == 'h':#�����ӵĵ�һ���ַ�Ϊh˵��������·��
                        try:
                            x=re.match(localfilter,tmpm.group(2))#�������ˣ�����������bistu.edu.cn����ֹ��ȡ̫����������
                        except:
                            x=''
                        try:
                            y=re.search('(.*)/(.*)',x.group(3))#��ȡ�������һ��/������ݣ�����Ϊ�գ���ʲô��û�У��˴�����tmpm.group(2)����Ϊ���ܴ���http://www.bistu.edu.cn�����
                        except:#���yûֵ����ô�͸���������
                            y=''
                        hzflag=1
                        if y:
                            try:
                                z=re.search('(.*)\.(.*)',y.group(2))#��ȡ��׺
                            except:
                                z=''
                            if z:
                                if z.group(2) <> 'html' and z.group(2) <> 'php' and z.group(2) <> 'htm':#����������ʽ�ĺ�׺��.doc��.rar��
                                    hzflag=0
                        if x and hzflag==1:
                            #�Ƚ��룬�����
                            try:
                                insertstr=tmpm.group(2)+":::"+tmpm.group(4).decode('UTF-8').encode('gbk')
                            except:
                                try:
                                    insertstr=tmpm.group(2)+":::"+tmpm.group(4)
                                except:
                                    insertstr=''
                                    #print tmpm.group(2)+"��˵������ʧ�ܣ�"
                            if insertstr:
                                newq.insert(0,insertstr)#����list�ײ�
                                count=count+1#������1
                        else:
                            continue
                    else:#���˵�������ʽ������
                        continue
                else:#�����ӣ�ֱ�������������ҳ����һ������
                    continue
    return

urlfilter=re.compile(r'<a(.*?)href="(.*?)"(.*?)>(.*?)</a>')
localfilter=re.compile('http(s?)://(.*?).bistu.edu.cn(.*)')
starturl='http://www.bistu.edu.cn/'
spider(starturl,urlfilter,localfilter)
