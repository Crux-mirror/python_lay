#codeing = utf-8

import pymysql


conn = pymysql.connect(host='10.0.86.32', port=3306,user='root',passwd='123456',
db='omms')
cur = conn.cursor()
cur.execute('SELECT COLUMN_NAME from information_schema.COLUMNS WHERE TABLE_NAME = "omms_way_point"')
print list(cur.fetchall())
cur.close()
conn.close()