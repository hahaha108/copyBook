from django.db import models
from django.urls import reverse

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=80, verbose_name='书名')
    cover = models.ImageField(upload_to='cover/',verbose_name='封面')
    author = models.CharField(max_length=50, verbose_name='作者')
    intro = models.TextField(verbose_name='简介')
    tag = models.ForeignKey('Tag',verbose_name='标签')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return /post/pk=self.pk/
        return reverse('book', kwargs={'pk': self.pk})


class Chapter(models.Model):
    number = models.IntegerField(verbose_name='章节号')
    title = models.CharField(max_length=50,verbose_name='章节名')
    content = models.TextField(verbose_name='内容')
    book = models.ForeignKey('Book',verbose_name='书名')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('chapter',kwargs={'pk':self.pk})


class Tag(models.Model):
    tagname = models.CharField(max_length=30,verbose_name='标签名')

    def __str__(self):
        return self.tagname

    def get_absolute_url(self):
        # return /post/pk=self.pk/
        return reverse('booklist', kwargs={'pk': self.pk})
