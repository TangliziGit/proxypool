# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis

from scrapy.exceptions import DropItem
from .rules import (
    DB_HOST, DB_PORT, DB_ID,
    DB_RAW_IPPOOL_NAME, DB_IPPOOL_NAME,
    THRESHOLD_SPEED,
)

class BasePipeline:
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # self._process_item
        # return item
        raise NotImplementedError

    # def from_crawler(cls, crawler):
    #    pass

class ProxyPipeline(BasePipeline):
    def process_item(self, item, spider):
        file=open("iplist.txt", "a")
        file.write('{"url":"%s"},\n'%(item["url"]))
        return item

class RedisRawProxyPipeline(BasePipeline):
    def __init__(self):
        self.rdb=redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID)
        # self.pipe=self.rdb.pipeline(transation=False)

    def process_item(self, item, spider):
        self.rdb.sadd(DB_RAW_IPPOOL_NAME, item["url"])
        return item

class RedisProxyPipeline(BasePipeline):
    def __init__(self):
        self.rdb=redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID)

    def process_item(self, item, spider):
        if item['speed']>THRESHOLD_SPEED:
            raise DropItem("proxy is too slow! (speed: %f)"%(item['speed']))
        self.rdb.zadd(DB_IPPOOL_NAME, item["speed"], item["url"])
        return item

