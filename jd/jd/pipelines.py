# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class JdPipeline(object):
    def open_spider(self,spider):
        client = pymongo.MongoClient(host='localhost',port=27017)
        mdb = client['jd']
        self.post = mdb['jd_pd']
        print('数据库连接成功')

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        print('bingo!!' * 6)
        return item

    def close_spider(self,spider):
        print('DONE.')
