from django.test import TestCase
from django.contrib.auth.models import User
from django.apps import apps

from blog.models import Category, Post


class CommentDataTestCase(TestCase):
    def setUp(self):
        apps.get_app_config('haystack').signal_processor.teardown()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin'
        )

        self.cate = Category.objects.create(name='测试')
        self.post = Post.objects.create(
            title='标题',
            body='内容',
            category=self.cate,
            user=self.user
        )
