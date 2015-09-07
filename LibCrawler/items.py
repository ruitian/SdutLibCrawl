# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VarifyItem(scrapy.Item):
    # define the fields for your item here like:
    number = scrapy.Field()
    passwd = scrapy.Field()
    status = scrapy.Field()


class AccountItem(scrapy.Item):
    number = scrapy.Field()
    passwd = scrapy.Field()
    books = scrapy.Field()
    name = scrapy.Field()
