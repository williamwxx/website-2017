import urllib2
import MySQLdb
import datetime
import demjson
import redis

now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
def redis_con():
    r = redis.Redis(host='192.168.30.128',port=6379,db=0)
    a= r.keys("/prod/zdcrm/zccrm-merchant/online/*")
    c= []
    for k in a:
        c.append(r.get(k))
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
    cur.execute("select url from monitor_url")
    info = cur.fetchall()
    for url_tub in info:
        url=url_tub[0]
        try:
            response = urllib2.urlopen(str(url),timeout = 2)
            html = response.read()
            sql = '''INSERT INTO monitor_json_data(url,downtime,json)VALUES('%s','%s','%s')'''%(str(url),str(now),str(html))
            cur.execute(sql)
        except:
           ejson={"status":"unknown","HOST":{"status":"unknown","host":"HOST IS ERROR"}}
           html=demjson.encode(ejson)
           sql = '''INSERT INTO monitor_json_data(url,downtime,json)VALUES('%s','%s','%s')'''%(str(url),str(now),str(html))
           cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])