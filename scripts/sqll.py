import urllib2
import MySQLdb
import datetime
import demjson
import redis

now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

try:
    conn= MySQLdb.connect(
        host='192.168.30.128',
        port = 3306,
        user='monitor',
        passwd='Monitor123Q',
        db ='monitor',
        )

    cur = conn.cursor()
    ipcur = conn.cursor()
    cur.execute("select url from monitor_url")
    info = cur.fetchall()
    for url_tub in info:
        url=url_tub[0]
        ipcur.execute("select ip_info from monitor_json_data where url='%s' ORDER by downtime desc LIMIT 1"%url)
        ip_info=ipcur.fetchall()
        for ipstr in ip_info:
            ip_list = list(eval(ipstr[0]))
            for ip in ip_list:
                print ip
                try:
                    response = urllib2.urlopen(str(ip),timeout = 2)
                    html = response.read()
                    sql = '''INSERT INTO monitor_ip_json_data(url,ip,downtime,ip_json)VALUES('%s','%s','%s','%s')'''%(str(url),str(ip),str(now),str(html))
                    cur.execute(sql)
                except:
                    ejson={"status":"UNKNOWN","HOST":{"status":"unknown","host":"HOST IS ERROR"}}
                    html=demjson.encode(ejson)
                    sql = '''INSERT INTO monitor_ip_json_data(url,ip,downtime,ip_json)VALUES('%s','%s','%s','%s')'''%(str(url),str(ip),str(now),str(html))
                    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])