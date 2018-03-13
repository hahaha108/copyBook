# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sqlite3


class BookspiderPipeline(object):
    def __init__(self):
        DBpath = os.getcwd() + '/db.sqlite3'
        self.con = sqlite3.connect(DBpath)
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        self.cur.execute("SELECT id FROM books_tag WHERE tagname = ?", (item['categoryName'],))
        tagID = self.cur.fetchone()
        if not tagID:
            self.cur.execute("INSERT INTO books_tag (tagname) VALUES (?)", (item['categoryName'],))
            self.con.commit()
            self.cur.execute("SELECT id FROM books_tag WHERE tagname = ?", (item['categoryName'],))
            tagID = self.cur.fetchone()
        tagID = tagID[0]
        print(tagID)

        self.cur.execute("SELECT id FROM books_book WHERE title = ?", (item['bookName'],))
        bookID = self.cur.fetchone()

        if not bookID:
            self.cur.execute('''
            INSERT INTO books_book (title, cover, author, intro, tag_id) VALUES (?,?,?,?,?)
            ''', (item['bookName'], item['cover'], item['author'], item['intro'], tagID))
            self.con.commit()
            self.cur.execute("SELECT id FROM books_book WHERE title = ?", (item['bookName'],))
            bookID = self.cur.fetchone()

        bookID = bookID[0]
        print(bookID)

        self.cur.execute('''INSERT INTO books_chapter (number, title, content, book_id) 
                        VALUES (?,?,?,?)''', (int(item['number']), item['chapterName'], item['chapterContent'], bookID))
        self.con.commit()
        return item

    def __del__(self):
        self.con.close()
