# copyBook
嘻嘻，这个网站内容好像挺有意思，不过，下一秒它们就是我的了

![](https://i.imgur.com/wcXoXsf.jpg)


----------

### 1.用到的技术：
爬虫框架：scrapy
数据库：sqlite
web框架：Django，bootstrap


### 2.Django数据模型与scrapy中item对应关系：
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

### 3.爬虫主逻辑：
爬虫基本是直接移植了我之前写的[全书网爬虫](https://github.com/hahaha108/Scrapy-FictionSpider "全书网爬虫")，主要业务逻辑没变，只是将最后分类存储为txt文本改变为存储到数据库，完善了部分代码，加入了文章简介、作者信息的提取。

### 4.Django图书网站：
在上述爬虫爬取完数据之后，便可以直接将存有数据的数据库移动到Django项目中进行展示。
本次使用了Django官方推荐的通用视图类，网站主要分为三个页面：主页（IndexView）、图书详情页（BookView）以及章节详情页(ChapterView)，前端模板页面使用了bootstrap框架，整个网站风格比较简洁，运行效果如下：

- **主页：**
![](https://i.imgur.com/uggyQYu.jpg)

![](https://i.imgur.com/EP6zF83.jpg)


- **图书详情页：**
![](https://i.imgur.com/j2UnkY1.jpg)

- **章节详情页：**
![](https://i.imgur.com/aBerDoX.jpg)
