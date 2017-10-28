#-*-  coding:utf-8 -*-

import MySQLdb as mysql
import time

def  Clear_data():
    conn = mysql.connect(host='127.0.0.1', user='cdndir',passwd='123.com', db='cdndir', charset='utf-8')
    cursor = conn.cursor()
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    sql = "delete from ccmapp_ccmrecord where DATE_FORMAT(date, '%Y-%m-%d') < %s " % date
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()


Clear_data()

