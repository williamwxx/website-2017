#coding: utf-8
import smtplib
from email.mime.text import MIMEText

sender = 'js_kashuo_pay@163.com'
receiver = 'wuxiangxiang@kashuo.com'
subject = MIMEText('<html><h1>wahahah</h1><br></html>','html','utf-8')
smtpserver = 'smtp.163.com'
username = 'js_kashuo_pay@163.com'
password = 'mjj12345'

msg = MIMEText('<html><h1>wahahah</h1><br><h1>lalalal</h1><br><a href=" http://www.ifeng.com ">凤凰卫视</a></html>','html','utf-8')
print msg.as_string()
print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
msg['Subject'] = subject.as_string()
msg['From'] = sender
msg['To'] = receiver
print msg
#print msg.as_string()
print "*****************************************************************"
print msg.as_string()


smtp = smtplib.SMTP()
smtp.connect('smtp.163.com')
smtp.login(username, password)
#smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()