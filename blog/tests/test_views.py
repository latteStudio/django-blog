from django.test import TestCase
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from django.utils import timezone
from datetime import timedelta


"""
思路：
    利用client实例，像特定的url发起请求，返回对返回的状态码、html内容，进行断言
    看是否符合预期的内容
        是否有正确的状态码
        模版填充了正确的变量
        渲染的html有预期内容
        没有文章时，是404
    
"""


class BlogDataTestCase(TestCase):
    def setUp(self):
        apps.get_app_config('haystack').signal_processor.teardown()

        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin',
        )

        self.cate1 = Category.objects.create(
            name='cate1'
        )
        self.cate2 = Category.objects.create(
            name='cate2'
        )

        self.tag1 = Tag.objects.create(
            name='tag1'
        )
        self.tag2 = Tag.objects.create(
            name='tag2'
        )

        self.post1 = Post.objects.create(
            title='post1',
            body='post1 body',
            category=self.cate1,
            user=self.user,

        )
        self.post1.tags.add(self.tag1)
        self.post1.save()

        self.post2 = Post.objects.create(
            title='post2',
            body='post2 body',
            category=self.cate2,
            user=self.user,
            created_time=timezone.now() - timedelta(days=100)
        )
        self.post2.save()


class CategoryViewTestCase(BlogDataTestCase):
    def setUp(self):
        super(CategoryViewTestCase, self).setUp()   #继承父类的数据
        self.url = reverse('blog:categories', kwargs={'category_id': self.cate1.pk})
        self.url2 = reverse('blog:categories', kwargs={'category_id': self.cate2.pk})

    def test_visit_a_nonexist_category(self):
        url = reverse('blog:categories', kwargs={'category_id': 100})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)

    def test_without_any_post_in_a_category(self):
        Post.objects.all().delete()
        res = self.client.get(self.url2)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(res, '没有该分类文章')

    def test_with_post(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(res, self.post1.title)
        self.assertIn('post_list', res.context)
        self.assertIn('page_obj', res.context)
        self.assertIn('is_paginated', res.context)
        self.assertEqual(res.context['post_list'].count(), 1)
        expected_qs = self.cate1.post_set.all().order_by('-created_time')
        self.assertQuerysetEqual(res.context['post_list'], [repr(p) for p in expected_qs])
