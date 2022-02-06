from django.test import TestCase
from blog.utils import Highlighter
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from django.utils import timezone
from datetime import timedelta
from blog.feed import AllPostsRssFeed
from django.template import Template, Context
from blog.templatetags.blog_extras import show_recently_post


class HighlighterTestCase(TestCase):
    def test_highlight(self):
        document = "这是一个比较长的标题，用于测试关键词高亮但不被截断。"
        highlighter = Highlighter("标题")
        expected = '这是一个比较长的<span class="highlighted">标题</span>，用于测试关键词高亮但不被截断。'
        self.assertEqual(highlighter.highlight(document), expected)

        highlighter = Highlighter("关键词高亮")
        expected = '这是一个比较长的标题，用于测试<span class="highlighted">关键词高亮</span>但不被截断。'
        self.assertEqual(highlighter.highlight(document), expected)
