# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MytestItem(scrapy.Item):
    # define the fields for your item here like:
    hlink=scrapy.Field()
    rest=scrapy.Field()
    comment=scrapy.Field()
    pass
