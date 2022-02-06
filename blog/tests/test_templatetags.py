from django.test import TestCase
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from django.utils import timezone
from datetime import timedelta
from blog.feed import AllPostsRssFeed
from django.template import Template, Context
from blog.templatetags.blog_extras import show_recently_post

class TemplateTagsTestCase(TestCase):
    def setUp(self):
        apps.get_app_config('haystack').signal_processor.teardown()

        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin',
        )

        self.cate = Category.objects.create(
            name='cate1'
        )
        self.ctx = Context()

    def test_show_recent_posts_with_posts(self):
        post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=self.cate,
            user=self.user,
        )
        context = Context(show_recently_post(self.ctx))
        template = Template(
            '{% load blog_extras %}'
            '{% show_recently_post %}'
        )
        expected_html = template.render(context)
        self.assertInHTML('<h3 class="widget-title">最新文章</h3>', expected_html)
        self.assertInHTML('<a href="{}">{}</a>'.format(post.get_absolute_url(), post.title), expected_html)
