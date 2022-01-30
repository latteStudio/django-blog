from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
import markdown
# Create your models here.
# 定义3个model，对应三张表：文章post、标签tag、分类category
from django.utils.html import strip_tags


# 标签
class Tag(models.Model):

    class Meta:
        verbose_name ='标签'
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# 分类
class Category(models.Model):

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# 文章
class Post(models.Model):
    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-created_time', 'title']

    title = models.CharField(verbose_name="标题", max_length=200)
    body = models.TextField(verbose_name="内容", max_length=600)
    created_time = models.DateTimeField("创建时间", default=timezone.now)
    modified_time = models.DateTimeField("修改时间")

    tags = models.ManyToManyField(to=Tag, verbose_name="标签", blank=True)                       #多对多，可为空
    category = models.ForeignKey(to=Category, verbose_name="分类", on_delete=models.CASCADE)     #一对多，外键，某分类删除，其下所有博客级联删除

    excerpt = models.CharField(max_length=50, verbose_name="摘要", blank=True)
    user = models.ForeignKey(to=User, verbose_name="作者", on_delete=models.CASCADE) # 对应author注意！

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        self.excerpt = strip_tags(md.convert(self.body))[:54]
        #     先用md实例，把md文档转为html格式，然后用django内置方法，把html标签去掉，再进行字符串切片，动态添加到post对象的摘要字段中
        #     然后在模版中引用
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):     # 在返回的博客的详情页面的模版使用，构造herf 超链接的 url，实现跳转功能
        return reverse('blog:detail', kwargs={
            'pk': self.id,
        })