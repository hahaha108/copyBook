# copyBook
嘻嘻，这个网站内容好像挺有意思，不过，下一秒它们就是我的了

![](https://i.imgur.com/wcXoXsf.jpg)


----------

### 一、用到的技术：
爬虫框架：scrapy <br> 数据库：sqlite <br> web框架：Django，bootstrap


### 二、数据模型建立：
本项目数据库表使用Django数据库迁移命令自动生成，为了保证爬虫爬取到的数据可以用于自己的Web项目，因此定义的scrapy中item和Django中的数据模型必须存在一定的对应关系，具体如下：

Book表：

```python

class Book(models.Model):

	#title对应item中的bookName
    title = models.CharField(max_length=80, verbose_name='书名')

	#cover对应item中的cover
    cover = models.ImageField(upload_to='cover/',verbose_name='封面')

	#author对应item中的author
    author = models.CharField(max_length=50, verbose_name='作者')

	#intror对应item中的intro
    intro = models.TextField(verbose_name='简介')

	#外键关联tag,对应category
    tag = models.ForeignKey('Tag',verbose_name='标签')
```
Chapter表：
```python

class Chapter(models.Model):

	#number对应item的number
    number = models.IntegerField(verbose_name='章节号')

	#title对应item的chapterName
    title = models.CharField(max_length=50,verbose_name='章节名')

	#content对应item的chapterContent
    content = models.TextField(verbose_name='内容')

	#外键关联book表
    book = models.ForeignKey('Book',verbose_name='书名')

```
Tag表：
```python
class Tag(models.Model):

	#Tag其实就是item中的category，因此tagname对应categoryName
    tagname = models.CharField(max_length=30,verbose_name='标签名')
```
对应关系搞好了后，爬虫下载下来的数据便可以直接用于自身web项目，无需多做别的操作。

### 三、爬虫主逻辑：
爬虫基本是直接移植了我之前写的[全书网爬虫](https://github.com/hahaha108/Scrapy-FictionSpider "全书网爬虫")，主要业务逻辑没变，只是将最后分类存储为txt文本改变为存储到数据库，完善了部分代码，加入了文章简介、作者信息的提取。

```python
class QuanshuwangSpider(scrapy.Spider):
    name = 'quanshuwang'
    allowed_domains = ['quanshuwang.com']
    start_urls = ['http://quanshuwang.com/']

    def parse(self, response):
		#提取网页上每个分类
        categorys = response.xpath("//ul[@class='channel-nav-list']/li/a")
		
		#循环遍历每个分类
        for category in categorys:
			#获取分类url链接
            categoryUrl = category.xpath("./@href").extract()[0]
			#获取分类名称
            categoryName = category.xpath("./text()").extract()[0]
			#传递
            yield scrapy.Request(categoryUrl,meta={"categoryName":categoryName},callback=self.getNext)
```
以上代码功能为提取网站各分类信息：
![](https://i.imgur.com/wqtpb9U.jpg)
<br> 

提取到各分类信息后，记录下分类的名称，然后循环遍历各分类,getNext方法用于遍历每个分类下的所有子页面，并提取所有书本的url
```python
    def getNext(self,response):
		#接收上面传过来的类别名称
        categoryName = response.meta["categoryName"]
		#获取下一页url
        nextUrl = response.xpath("//a[@class='next']/@href").extract()[0]
		#获取当前页面上所有图书的url
        urls = response.xpath("//ul[@class='seeWell cf']/li/span/a[1]/@href").extract()
        for url in urls:
            yield scrapy.Request(url,meta={"categoryName":categoryName},callback=self.getBooks)
		#递归终止条件：不存在下一页则结束
        if not response.xpath("//a[@class='next']/@href").extract():
            pass
        else:
			#若存在下一页则调用自己，继续提取下一页
            yield scrapy.Request(nextUrl,meta={"categoryName":categoryName},callback=self.getNext)
```
![](https://i.imgur.com/HPO5zXY.jpg)
<br> 

接下来用getBooks方法爬取每本图书的详情页，利用xpath可以很方便的提取到书名，作者，简介，封面图片等各类信息：
```python
    def getBooks(self,response):
		#接收参数
        categoryName = response.meta["categoryName"]
		#xpath提取各类信息
        bookName = response.xpath("//div[@class='b-info']/h1/text()").extract()[0]
        bookUrl = response.xpath("//div[@class='b-oper']/a[@class='reader']/@href").extract()[0]
        author = response.xpath("//div[@class='bookDetail']/dl[@class='bookso']/dd[1]/text()").extract()[0].strip()
        intro = response.xpath("//div[@id='waa']/text()").extract()[0].strip()
        imgUrl = response.xpath("//a[@class='l mr11']/img/@src").extract()[0]

		#保存封面图片（应该写在pipelines.py里面的，为了方便就直接写这里了）
        filename = bookName + '.jpg'
        dirpath = './cover'
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        filepath = os.path.join(dirpath, filename)
        urllib.request.urlretrieve(imgUrl, filepath)
        cover = 'cover/' + filename

        # 继续下一个页面
        yield scrapy.Request(bookUrl,meta={"categoryName":categoryName,
                                           'bookName':bookName,
                                           'bookUrl':bookUrl,
                                           'author':author,
                                           'intro':intro,
                                           'cover':cover
                                           },callback=self.getChapter)
```
![](https://i.imgur.com/4uBvREr.jpg)
<br> 

getChapter方法用于提取书本各章节的顺序以及名称等信息，并获取到所有章节内容对应的url
```python
    def getChapter(self,response):
		#接收参数
        categoryName = response.meta["categoryName"]
        bookName = response.meta["bookName"]
        bookUrl = response.meta["bookUrl"]
        author = response.meta["author"]
        intro = response.meta["intro"]
        cover = response.meta["cover"]

		#提取页面上所有章节
        chapters = response.xpath("//div[@class='clearfix dirconone']//li/a")
		#number用于记录章节顺序，防止错位
        number = 0

		#循环遍历每个章节
        for chapter in chapters:
            number += 1
			#获取章节名称、url
            chapterName = chapter.xpath("./text()").extract()[0]
            chapterUrl = chapter.xpath("./@href").extract()[0]


			#继续传递
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
```

![](https://i.imgur.com/n5nNd8k.jpg)
<br> 

getContent方法为提取信息的最后一步，这一步可以获取到章节的详细内容，生成并返回item
```python
    def getContent(self,response):
		#接收传过来的参数
        categoryName = response.meta["categoryName"]
        bookName = response.meta["bookName"]
        bookUrl = response.meta["bookUrl"]
        chapterName = response.meta["chapterName"]
        chapterUrl = response.meta["chapterUrl"]
        author = response.meta["author"]
        intro = response.meta["intro"]
        cover = response.meta["cover"]
        number = response.meta["number"]

		#提取章节的文本内容并调整格式
        chapterContent = "".join(response.xpath("//div[@id='content']/text()").extract())
        chapterContent = chapterContent.replace(r'''
''',"<br>")
        chapterContent = chapterContent.replace(r" ", "&nbsp")

		#生成并返回item
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
```
![](https://i.imgur.com/vzJzxUA.jpg)
至此爬虫的主要代码已经基本写完了，剩下的就是信息存储到数据库的各种sql语句了，若程序执行时间够久，理论上可以爬取到此网站上的全部书本。
### 四、Django图书网站：
在上述爬虫爬取到数据之后，便可以直接将存有数据的数据库移动到Django项目中，从而达到建立自己的图书网站的目的。
本次使用了Django官方推荐的通用视图类，网站主要分为三个页面：主页（IndexView）、图书详情页（BookView）以及章节详情页(ChapterView)，前端模板页面使用了bootstrap框架，整个网站风格比较简洁，运行效果如下：

- **主页：**
![](https://i.imgur.com/uggyQYu.jpg)

![](https://i.imgur.com/EP6zF83.jpg)


- **图书详情页：**
![](https://i.imgur.com/j2UnkY1.jpg)

- **章节详情页：**
![](https://i.imgur.com/aBerDoX.jpg)
<be>
一个专属的，没有广告的图书网站就诞生了。→_→