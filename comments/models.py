from django.db import models
from django.utils import timezone
# Create your models here.


from django.db.models.signals import post_delete, post_save
from django.core.cache import cache
from datetime import datetime




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


def change_comment_updated_at(sendef=None, instance=None, *args, **kwargs)
    cache.set("comment_updated_at", datetime.utcnow())


post_save.connect(receiver=change_comment_updated_at, sender=Comments)
post_delete.connect(receiver=change_comment_updated_at, sender=Comments)
