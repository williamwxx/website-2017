import threadpool
import time
import urllib2
import datetime
import MySQLdb

now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
try:
    url=[]
    urlkey=[]
    conn= MySQLdb.connect(
        host='58.210.177.89',
        port = 33639,
        user='ksmonitor_user',
        passwd='ksdev.mysql.ksmonitor_password@2017',
        db ='ksmonitor_dev',
        )
    cur = conn.cursor()
    cur.execute("select url,urlkey from monitor_url")
    info = cur.fetchall()
    for url_tub in info:
        url.append(url_tub[0])
        urlkey.append(url_tub[1])
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
cur.close()
conn.commit()
conn.close()

def myRequest(url):
    conn= MySQLdb.connect(
    host='58.210.177.89',
    port = 33639,
    user='ksmonitor_user',
    passwd='ksdev.mysql.ksmonitor_password@2017',
    db ='ksmonitor_dev',
    )
    cur = conn.cursor()
    print url
    print urlkey
#    try:
#        resp = urllib2.urlopen("http://%s/health"%url,timeout=1)
#        request=resp.read()
#        print request
#        sql = '''INSERT INTO test(name,passwd)VALUES('%s','%s')'''%(str(url),"111111")
#        cur.execute(sql)
#    except:
#        print "Error"
#        sql = '''INSERT INTO test(name,passwd)VALUES('%s','%s')'''%(str(url),"222222")
#        cur.execute(sql)
#    cur.close()
#    conn.commit()
    conn.close()

def timeCost(request, n):
  print "Elapsed time: %s" % (time.time()-start)


start = time.time()
pool = threadpool.ThreadPool(10)
reqs = threadpool.makeRequests(myRequest,url,timeCost)
[ pool.putRequest(req) for req in reqs ]
pool.wait()



'''
    cur.execute("select url,urlkey from monitor_url")
    info = cur.fetchall()
    for url_tub in info:
        url.append(url_tub[0])
        urlkey.append(url_tub[1])
    print url
    print urlkey
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
'''