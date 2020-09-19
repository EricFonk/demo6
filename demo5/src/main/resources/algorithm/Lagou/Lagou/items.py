# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionname= scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    detail = scrapy.Field()


