import sqlite3

item = {
    'categoryName':'kongbu',
    'cover':'cover/nahan.jpg',
    'author':'zhangsan',
    'intro':'santixiaoshuo',
    'bookName':'santi',
    'chapterName':'santi01',
    'chapterContent':'zhenwen6666666666666sssssssssssssssssssssssss',
}

DBpath = '../db.sqlite3'
con = sqlite3.connect(DBpath)
cur = con.cursor()
cur.execute("SELECT id FROM books_tag WHERE tagname = ?",(item['categoryName'],))
tagID = cur.fetchone()
if not tagID:
    cur.execute("INSERT INTO books_tag (tagname) VALUES (?)", (item['categoryName'],))
    con.commit()
    cur.execute("SELECT id FROM books_tag WHERE tagname = ?", (item['categoryName'],))
    tagID = cur.fetchone()
tagID = tagID[0]
print(tagID)

cur.execute("SELECT id FROM books_book WHERE title = ?",(item['bookName'],))
bookID = cur.fetchone()

if not bookID:
    cur.execute('''
    INSERT INTO books_book (title, cover, author, intro, tag_id) VALUES (?,?,?,?,?)
    ''',(item['bookName'],item['cover'],item['author'],item['intro'],tagID))
    con.commit()
    cur.execute("SELECT id FROM books_book WHERE title = ?", (item['bookName'],))
    bookID = cur.fetchone()

bookID = bookID[0]
print(bookID)

cur.execute('''INSERT INTO books_chapter (number, title, content, book_id) 
                VALUES (?,?,?,?)''',(1,item['chapterName'],item['chapterContent'],bookID))
con.commit()
