from django.test import TestCase
from django.apps import apps
from blog.models import Post, Category, Tag
from django.contrib.auth.models import User
from django.urls import reverse


"""
测试内容：
    __str__方法返回post对象的title字符串
    save()方法会自动创建，创建时间，和摘要
    get_absolute_url 返回文章的详情试图对应的url
    update_views 将views字段+1
"""


class PostModelTestCase(TestCase):
    def setUp(self):
        # 设置初始化模型实例数据
        # 断开haystack的sinal，测试文章，无需索引
        apps.get_app_config('haystack').signal_processor.teardown()

        user = User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin'

        )

        cate = Category.objects.create(name='测试')
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=cate,
            user=user,
        )

    def test_str_repr(self):
        self.assertEqual(self.post.__str__(), self.post.title)

    def test_auto_populate_modified_time(self):
        self.assertIsNotNone(self.post.modified_time)

        old_modified_time = self.post.modified_time
        self.post.body = '内容更新'
        self.post.sava()
        self.post.refresh_from_db()

        self.assertTrue(self.post.modified_time > old_modified_time)

    def test_get_abs_url(self):
        expected_url = reverse('blog:detail', kwargs={
            'pk': self.post.pk
        })
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_update_views(self):

        self.assertEqual(self.post.views, 0)

        self.post.update_views()
        self.post.refresh_from_db()

        self.assertEqual(self.post.views, 1)
