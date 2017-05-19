#!/usr/bin/env python
#--coding: utf-8--

import MySQLdb
import urllib2
import demjson
import datetime
import threadpool
now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

def urllist():
    url=[]
    try:
        conn= MySQLdb.connect(
            host='172.17.0.103',
            port = 33639,
            user='ksmonitor_user',
            passwd='ksdev.mysql.ksmonitor_password@2017',
            db ='ksmonitor_dev',
            )
        cur = conn.cursor()
        cur.execute("select url from monitor_url")
        info = cur.fetchall()
        for url_tub in info:
            url.append(url_tub[0])
        return url
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def k8s(key):
    iplist=[]
    try:
        response = urllib2.urlopen("http://172.17.0.100:8080/api/v1/namespaces/default/endpoints/%s"%key,timeout = 1)
        k8s_str = response.read()
        k8s_json=demjson.decode(k8s_str)
        ip_port=str(k8s_json["subsets"][0]["ports"][0]['port'])
        for ip in k8s_json["subsets"][0]["addresses"]:
            iplist.append(str(ip["ip"])+":"+ip_port)
    except:
        ip="%s is Error"%key
        iplist.append(ip)
    return str(iplist)


def myRequest(url):
    try:
        conn= MySQLdb.connect(
            host='172.17.0.103',
            port = 33639,
            user='ksmonitor_user',
            passwd='ksdev.mysql.ksmonitor_password@2017',
            db ='ksmonitor_dev',
            )
        cur = conn.cursor()
        cur.execute("select urlkey from monitor_url where url = '%s'"%url)
        info = cur.fetchall()
        for url_tub in info:
            urlkey=url_tub[0]
            ip_info=k8s(urlkey)
        try:
                response = urllib2.urlopen("http://%s/health"%url,timeout = 1)
                html = response.read()
                check_json = demjson.decode(html)
                sql = '''INSERT INTO monitor_json_data(url,ip_info,downtime,json)VALUES('%s',"%s",'%s','%s')'''%(str(url),ip_info,str(now),str(html))
                cur.execute(sql)
        except:
                ejson={"status":"DOWN","HOST":{"status":"UNKNOW","host":"HOST IS ERROR"}}
                html=demjson.encode(ejson)
                sql = '''INSERT INTO monitor_json_data(url,ip_info,downtime,json)VALUES('%s',"%s",'%s','%s')'''%(str(url),ip_info,str(now),str(html))
                cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


pool = threadpool.ThreadPool(10)
reqs = threadpool.makeRequests(myRequest,urllist())
[ pool.putRequest(req) for req in reqs ]
pool.wait()


