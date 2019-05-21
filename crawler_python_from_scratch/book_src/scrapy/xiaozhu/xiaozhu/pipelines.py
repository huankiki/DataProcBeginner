# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class XiaozhuPipeline(object):
    def process_item(self, item, spider):
        fp = open('C:/Users/LP/Desktop/xiaozhu.txt','a+')
        fp.write(item['title']+'\n')
        fp.write(item['address']+'\n')
        fp.write(item['price'] + '\n')
        fp.write(item['lease_type'] + '\n')
        fp.write(item['suggestion'] + '\n')
        fp.write(item['bed'] + '\n')
        return item
