from django.db import models
from django.utils import timezone
# Create your models here.


class Comments(models.Model):
    name = models.CharField('名字', max_length=20)
    email = models.EmailField('邮箱')
    text = models.TextField('内容')
    website = models.URLField('评论者网址', blank=True)

    created_time = models.DateTimeField('评论时间', default=timezone.now)
    post = models.ForeignKey(to='blog.Post', verbose_name='关联博客', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['-created_time', 'name']

    def __str__(self):
        return "{}:{}".format(self.name, self.text[:20])


