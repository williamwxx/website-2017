# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpRequest,request,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from monitor import models
import datetime
import time
import threading
import urllib2
import demjson
import codecs
import re
from django.core.urlresolvers import reverse


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
"""
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
"""
def ipinfo(url):
    for url_json in models.json_data.objects.raw('''select id,ip_info,downtime from monitor_json_data where url='%s' ORDER BY downtime DESC LIMIT 1'''%(str(url))):
        iplist=url_json.ip_info
        list2 = list(eval(iplist))
        ipnum=len(list2)+1
        iplist_dict={}
        for ip in list2:
            for ip_json in models.ip_json_data.objects.raw('''select id,ip,ip_json from monitor_ip_json_data where ip='%s' ORDER BY downtime DESC LIMIT 1'''%(str(ip))):
                try:
                    ip_json_dict = demjson.decode(ip_json.ip_json)
                    ip_json_status=ip_json_dict["status"]
                except:
                    ip_json_status="UNKNOWN"
                iplist_dict[ip]=ip_json_status
        return (len(list2),ipnum,iplist_dict)


def index(request):
    print datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    list=[]
    for monitor_url in models.url.objects.raw('''select id,host,url from monitor_url'''):
        for url_json in models.json_data.objects.raw('''select id,json,downtime from monitor_json_data where url='%s' ORDER BY downtime DESC LIMIT 1'''%(monitor_url.url)):
            monitor_url_id=monitor_url.id
            json_host=monitor_url.host
            json_url=monitor_url.url
            try:
                json_dict = demjson.decode(url_json.json)
                json_status=json_dict["status"]
            except:
                json_statu="UNKNOW"
            ipinfotub = ipinfo(json_url)
            ipsum = ipinfotub[0]
            htmlsum = ipinfotub[1]
            iplist_dict = demjson.encode(ipinfo(json_url)[2])
            str ='''{'id':%s,'host':'%s','url':'%s','status':'%s','hostsum':'共%d台','ipnum':'%s','iplist':%s}'''%(monitor_url_id,json_host,json_url,json_status,ipsum,htmlsum,iplist_dict)
            index_dict=demjson.decode(str)
            list.append(index_dict)
    print datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    return render_to_response("index.html",{'list':list})

def ip_list(request):
    list1=[]
    page=request.GET.get('host')
    for monitor_url in models.url.objects.raw('''select id,host,url from monitor_url where id = %s'''%str(page)):
        if not monitor_url is None:
            host=monitor_url.host
            url=monitor_url.url
            for url_json in models.json_data.objects.raw('''select id,ip_info,downtime from monitor_json_data where url='%s' ORDER BY downtime DESC LIMIT 1'''%url):
                iplist=url_json.ip_info
                list2 = list(eval(iplist))
                for ip in list2:
                    for ip_json in models.ip_json_data.objects.raw('''select id,ip,downtime,ip_json from monitor_ip_json_data where ip='%s' ORDER BY downtime DESC LIMIT 1'''%ip):
                        ip=ip_json.ip
                        ip_json_dict = demjson.decode(ip_json.ip_json)
                        ip_json_dict_key=[]
                        ip_json_time=ip_json.downtime
                        for k in ip_json_dict:
                            ip_json_dict_key.append(k)
                        ip_json_dict_key.remove("status")
                        for kk in ip_json_dict_key:
                            decs=""
                            for des in ip_json_dict[kk]:
                                if des != "status":
                                    decs=decs+des+":"+str((ip_json_dict)[kk][des])+" "
                            ip_idct_str ='''{'host':'%s','url':'%s','ip':'%s','service':'%s','status':'%s','downtime':'%s','decs':'%s'}'''%(host,url,ip,kk,ip_json_dict[kk]["status"],ip_json_time,decs)
                            index_dict=demjson.decode(ip_idct_str)
                            list1.append(index_dict)
    return render_to_response("list.html",{'list':list1})