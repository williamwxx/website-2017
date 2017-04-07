# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpRequest,request
from django.shortcuts import render
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from monitor import models
import threading
import urllib2
import demjson

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
    
    return render_to_response("index.html",{"dicts":dicts})