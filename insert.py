#coding=utf8
import mysql
import time 

row = {'desk': '0001', 'comment': u'这个好难吃', 'stamp': time.time()}

for i in range(300):
    mysql.insert('comment', row)
