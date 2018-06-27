# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RawProxyUrlItem(scrapy.Item):
    # url="http://0.0.0.0:0"
    url=scrapy.Field()

class ProxyUrlItem(scrapy.Item):
    url=scrapy.Field()
    speed=scrapy.Field()

class ProxypoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
