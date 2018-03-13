# -*- coding: utf-8 -*-
import os

from bookspider.items import BookSpiderItem
import scrapy
import urllib


class QuanshuwangSpider(scrapy.Spider):
    name = 'quanshuwang'
    allowed_domains = ['quanshuwang.com']
    start_urls = ['http://quanshuwang.com/']

    def parse(self, response):
        categorys = response.xpath("//ul[@class='channel-nav-list']/li/a")

        for category in categorys:
            categoryUrl = category.xpath("./@href").extract()[0]
            categoryName = category.xpath("./text()").extract()[0]
            # print(categoryName, ":", categoryUrl)
            # while self.getNext(categoryUrl) != -1:
            #     print(categoryUrl)
            #     categoryUrl = self.getNext(categoryUrl)
            yield scrapy.Request(categoryUrl,meta={"categoryName":categoryName},callback=self.getNext)



    def getNext(self,response):
        # response.encoding = "gbk"

        categoryName = response.meta["categoryName"]

        nextUrl = response.xpath("//a[@class='next']/@href").extract()[0]

        urls = response.xpath("//ul[@class='seeWell cf']/li/span/a[1]/@href").extract()
        for url in urls:
            yield scrapy.Request(url,meta={"categoryName":categoryName},callback=self.getBooks)

        # html = lxml.etree.HTML(response.text)

        if not response.xpath("//a[@class='next']/@href").extract():
            pass
        else:
            yield scrapy.Request(nextUrl,meta={"categoryName":categoryName},callback=self.getNext)


    def getBooks(self,response):
        categoryName = response.meta["categoryName"]

        bookName = response.xpath("//div[@class='b-info']/h1/text()").extract()[0]
        bookUrl = response.xpath("//div[@class='b-oper']/a[@class='reader']/@href").extract()[0]
        author = response.xpath("//div[@class='bookDetail']/dl[@class='bookso']/dd[1]/text()").extract()[0].strip()
        intro = response.xpath("//div[@id='waa']/text()").extract()[0].strip()

        imgUrl = response.xpath("//a[@class='l mr11']/img/@src").extract()[0]

        filename = bookName + '.jpg'
        dirpath = './cover'
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        filepath = os.path.join(dirpath, filename)
        urllib.request.urlretrieve(imgUrl, filepath)

        cover = 'cover/' + filename
        # print(bookName,':',bookUrl)
        # print("------------------------------------------------------")
        yield scrapy.Request(bookUrl,meta={"categoryName":categoryName,
                                           'bookName':bookName,
                                           'bookUrl':bookUrl,
                                           'author':author,
                                           'intro':intro,
                                           'cover':cover
                                           },callback=self.getChapter)


    def getChapter(self,response):
        categoryName = response.meta["categoryName"]
        bookName = response.meta["bookName"]
        bookUrl = response.meta["bookUrl"]
        author = response.meta["author"]
        intro = response.meta["intro"]
        cover = response.meta["cover"]


        chapters = response.xpath("//div[@class='clearfix dirconone']//li/a")
        number = 0

        for chapter in chapters:
            number += 1
            chapterName = chapter.xpath("./text()").extract()[0]
            chapterUrl = chapter.xpath("./@href").extract()[0]
            # print(categoryName)
            # print('          -----------',bookName,':',bookUrl)
            # print('                         --------------',chapterName,':',chapterUrl)
            # print("-------------------------------------------------------------------")
            yield scrapy.Request(chapterUrl,meta={
                'categoryName':categoryName,
                'bookName': bookName,
                'bookUrl': bookUrl,
                'chapterName': chapterName,
                'chapterUrl': chapterUrl,
                'author': author,
                'intro': intro,
                'cover': cover,
                'number':number
            },callback=self.getContent)

    def getContent(self,response):
        categoryName = response.meta["categoryName"]
        bookName = response.meta["bookName"]
        bookUrl = response.meta["bookUrl"]
        chapterName = response.meta["chapterName"]
        chapterUrl = response.meta["chapterUrl"]
        author = response.meta["author"]
        intro = response.meta["intro"]
        cover = response.meta["cover"]
        number = response.meta["number"]

        chapterContent = "".join(response.xpath("//div[@id='content']/text()").extract())
        chapterContent = chapterContent.replace(r'''
''',"<br>")
        chapterContent = chapterContent.replace(r" ", "&nbsp")

        item = BookSpiderItem()
        item["categoryName"] = categoryName
        item["bookName"] = bookName
        item["bookUrl"] = bookUrl
        item["chapterName"] = chapterName
        item["chapterUrl"] = chapterUrl
        item["chapterContent"] = chapterContent
        item["author"] = author
        item["intro"] = intro
        item["cover"] = cover
        item["number"] = number

        return item





