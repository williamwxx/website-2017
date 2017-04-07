#!/usr/bin/env python
# -*- coding:utf-8 -*-
import MySQLdb
import urllib2
import datetime
import time
try:
    conn=MySQLdb.connect(host='192.168.30.128',user='monitor',passwd='Monitor123Q',db='data',port=3306)
    cur=conn.cursor()
    cur.execute('select * from url_data')
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
