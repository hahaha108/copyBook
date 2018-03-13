# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    categoryName = scrapy.Field()
    bookName = scrapy.Field()
    bookUrl = scrapy.Field()
    chapterName = scrapy.Field()
    chapterUrl = scrapy.Field()
    chapterContent = scrapy.Field()

    cover = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()
    number = scrapy.Field()


