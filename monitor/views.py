# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpRequest,request
from django.shortcuts import render
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from monitor import models
import datetime
import time
import threading
import urllib2
import demjson

#递归嵌入式字典
def list_all_dict(dict_a):
    a=[]
    if isinstance(dict_a,dict) : #使用isinstance检测数据类型
        for x in range(len(dict_a)):
            temp_key = dict_a.keys()[x]
            temp_value = dict_a[temp_key]
            a.append(temp_key)
#            print"%s : %s" %(temp_key,temp_value)
            list_all_dict(temp_value) #自我调用实现无限遍历
    return a

# Create your views here.
'''
def index(request):
    dicts ={ "status" : "DOWN",
    "myHealthCheck" : {
        "status" : "DOWN",
        "Error Code" : 1,
        "Description" : "You custom MyHealthCheck endpoint is down"
     },
     "diskSpace" : {
         "status" : "UP",
         "free" : 209047318528,
         "threshold" : 10485760
     }
}
    try:
        response = urllib2.urlopen('http://ip.taobao.com/service/getIpInfo.php?ip=58.210.151.1,timeout = 3')
        html = response.read()
        data1  = demjson.encode(html)
        print data1
    except:
        print "error"
    return render_to_response("index.html",{"dicts":dicts,})

def index(request):
    host = "V1"
    dicts ={ "status" : "DOWN",
    "myHealthCheck" : {
        "status" : "DOWN",
        "Error Code" : 1,
        "Description" : "You custom MyHealthCheck endpoint is down"
     },
     "diskSpace" : {
         "status" : "UP",
         "free" : 209047318528,
         "threshold" : 10485760
     }
}
    data2 = demjson.encode(dicts)
    print(dicts["diskSpace"]["status"])
#    print(data2['myHealthCheck']['status'])
    for i in models.url.objects.raw(''select id,host,url from monitor_url''):
        requset = urllib2.Request(i.url)
        try:
            response=urllib2.urlopen(requset,timeout=3)
            html = response.read()
            data1 = demjson.encode(html)
            print i.host
            print data1
        except urllib2.URLError, e:
            print e.reason
        except:
            print "error"
#    return render(request, "index.html")
    return render_to_response("index.html",{"dicts":data1,})
'''

def index(request):
 #   try:
        list=[]
#读取数据库URL数据量
        for monitor_url in models.url.objects.raw('''select id,url from monitor_url'''):
#获取URL对应的JSON报文
            for url_json in models.json_data.objects.raw('''select id,json,downtime from monitor_json_data where url='%s' ORDER BY downtime DESC LIMIT 1'''%(str(monitor_url.url))):
                json_url=monitor_url.url
                json_time=url_json.downtime
                json_dict = demjson.decode(url_json.json)
                json_dict_key=[]
#遍历字典服务EKY值并删除主机状态
                for k in json_dict:
                    json_dict_key.append(k)
                json_dict_key.remove("status")
#通过KEY值组装成显示的字典集合
                for kk in json_dict_key:
                    decs=""
                    for des in json_dict[kk]:
                        print des
                        if des != "status":
                           decs=decs+des+":"+str(json_dict[kk][des])+","
                    c={"host":json_url,
                    "server":kk,
                    "serstatus":json_dict[kk]["status"],
                    "date":json_time,
                    "decs":str(decs)}
                    list.append(c)
        print list
        return render_to_response("index.html",{'list':list})
#    except:
#        print "error"
