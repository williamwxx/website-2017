from django.core.cache import cache
import redis
import MySQLdb
import urllib2
import demjson
import datetime
import time
now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

def redis_con(key):
    print key
    r = redis.Redis(host='192.168.30.128',port=6379,db=0)
    a= r.keys("%s*"%key)
    c= []
    for k in a:
        c.append(r.get(k))
    print c
    return c

try:
    conn= MySQLdb.connect(
        host='192.168.30.128',
        port = 3306,
        user='monitor',
        passwd='Monitor123Q',
        db ='monitor',
        )

    cur = conn.cursor()
    cur.execute("select url,urlkey from monitor_url")
    info = cur.fetchall()
    for url_tub in info:
        url=url_tub[0]
        urlkey=url_tub[1]
        try:
            response = urllib2.urlopen(str(url),timeout = 1)
            html = response.read()
            sql = '''INSERT INTO monitor_json_data(url,ip_info,downtime,json)VALUES('%s',"%s",'%s','%s')'''%(str(url),str(redis_con(urlkey)),str(now),str(html))
            cur.execute(sql)
        except:
            ejson={"status":"UNKNOW","HOST":{"status":"UNKNOW","host":"HOST IS ERROR"}}
            html=demjson.encode(ejson)
            sql = '''INSERT INTO monitor_json_data(url,ip_info,downtime,json)VALUES('%s',"%s",'%s','%s')'''%(str(url),str(redis_con(urlkey)),str(now),str(html))
            cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])



