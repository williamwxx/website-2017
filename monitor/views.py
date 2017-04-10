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
    try:
        response = urllib2.urlopen('http://hdpz.dev.kashuo.net/health',timeout = 2)
        html = response.read()
        print type(html)
        data1  = demjson.decode(html)
    except:
        print "error"

#    a=list_all_dict(data1)
#    print a
#    a.remove("status")
#   Description=a.remove()
    d=[]
    for k in data1:
        d.append(k)
    d.remove("status")
    list=[]
    for i in d:
        print data1[i]
        decs=""
        for kk in data1[i]:
            if kk != "status":
                decs=decs+kk+":"+str(data1[i][kk])+","
        c={"host":"http://hdpz.dev.kashuo.net/health",
          "server":i,
          "serstatus":data1[i]["status"],
          "date":"20170101",
          "decs":str(decs)}
        list.append(c)
    print list
    return render_to_response("index.html",{'list':list})

'''
  try:
        response = urllib2.urlopen('http://hdpz.dev.kashuo.net/health,timeout = 2')
        html = response.read()
        data1  = demjson.encode(html)
        print data1
    except:
        print "error"

    str12='{ "status" : "DOWN", "CPU" : {"status" : "DOWN",\
        "Error Code" : 1,\
        "Description" : "You custom MyHealthCheck endpoint is down"\
     },"diskSpace" : {"status" : "UP","free" : 209047318528,"threshold" : 10485760}}'
    print type(str12)
    dict12 = demjson.decode(str12)
    print 111111
    a=list_all_dict(dict12)
    a.remove("status")
#    Description=a.remove()
    list=[]
    for i in a:
       print i
       c={"host":"host1",
          "server":i,
          "serstatus":dict12[i]["status"],
          "date":"20170101",
          "decs":dict12[i]}
       list.append(c)
    print list
    return render_to_response("index.html",{'list':list})
'''