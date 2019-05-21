# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class JianshuitPipeline(object):
    def __init__(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='mydb', port=3306, charset='utf8')
        cursor = conn.cursor()
        self.post = cursor
    def process_item(self, item, spider):
        cursor = self.post
        cursor.execute("use mydb")
        sql = "insert into jianshu1 (user,time,title,view,comment,lik,gain) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(item['user'],item['time'],item['title'],item['view'],item['comment'],item['like'],item['gain']))
        cursor.connection.commit()
        return item
