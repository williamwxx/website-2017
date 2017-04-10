import urllib2
import MySQLdb
#import demjson

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
            print html
        except:
            html={"status":"unknown","HOST":{"status":"unknown","host":"HOST IS ERROR"}}
            print html

    cur.close()
    conn.commit()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])