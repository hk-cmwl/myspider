# -*- coding: gbk -*-
import urllib2
import re

def spider(starturl,urlfilter,localfilter):
    oldq=[]
    newq=[]
    result=[]
    newq.append(starturl)
    count=0
    while newq:#ֻҪnewq���зǿ�
        flag=0
        newurl=newq.pop()#����listβ��
        for oldurl in oldq:#����url�Ƿ��Ѿ��������
            if oldurl == newurl:#��url�Ѿ����������
                #print oldurl+'�ѱ��������'
                flag=1
                break
        if flag == 0:#��urlδ�������
            if newurl:
                print '���ڴ������ӣ�'+newurl
                oldq.append(newurl)#���뱻�������
                try:
                    context=urllib2.urlopen(newurl,timeout=20).read()#��ȡ��URL��Ӧ��ҳ��Ϣ
                except:
                    print '�޷��������ӣ�'+newurl
                    continue
                m=re.finditer(urlfilter,context)
                for tmpm in m:
                    if tmpm.group(2):#�ǿ�����
                        if tmpm.group(2)[0] == '.':#�����ӵ�һ���ַ�Ϊ.˵�������·����Ҫ������ش���
                            #��ʱ����
                            continue
                        elif tmpm.group(2)[0] == 'h':#�����ӵĵ�һ���ַ�Ϊh˵��������·������������������bistu.edu.cn
                            try:
                                x=re.match(localfilter,tmpm.group(2))#��������
                            except:
                                x=''
                            try:
                                y=re.search('(.*)/(.*)',tmpm.group(2))#��ȡ/������
                            except:#���yûֵ����ô�͸���������
                                y=''
                            hzflag=1
                            if y:
                                try:
                                    z=re.search('(.*)\.(.*)',y.group(2))#��ȡ��׺
                                except:
                                    z=''
                                if z:
                                    if z.group(2) <> 'html' and z.group(2) <> 'php' and z.group(2) <> 'htm':#����к�׺����ΪҪ��ƥ���׺
                                        hzflag=0
                            if x and hzflag==1:
                                count=count+1
                                newq.insert(0,tmpm.group(2))#����list�ײ�
                                try:
                                    print tmpm.group(2)+"  ˵����  "+tmpm.group(4).decode('UTF-8').encode('gbk')
                                except:
                                    try:
                                        print tmpm.group(2)+"  ˵����  "+tmpm.group(4)
                                    except:
                                        print tmpm.group(2)+"��˵������ʧ�ܣ�"
                            else:
                                continue
                        else:#���˵�������ʽ������
                            continue
                    else:#�����ӣ�ֱ������
                        continue
            else:
                continue
    return

urlfilter=re.compile(r'<a(.*?)href="(.*?)"(.*?)>(.*?)</a>')
localfilter=re.compile('http(s?)://(.*?).bistu.edu.cn')
starturl='http://www.bistu.edu.cn/'
spider(starturl,urlfilter,localfilter)
