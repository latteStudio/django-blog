from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
# Create your views here.

from .models import Post, Category, Tag
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def index(request):
    post_list = Post.objects.all().order_by('-created_time')   # -为逆序排序
    return render(request, 'blog/index.html', context={
        'post_list': post_list,
    })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量+1
    post.update_views()

    md = markdown.Markdown(extensions=[   # 将数据库中存储的markdown格式的文本，经由markdown库转为html格式，然后再结合模版渲染！
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)   # 对post的body进行转换

    match = re.search(r'<div class="toc">\s*<ul>(.+)</ul>\s*</div>', md.toc, re.S)

    post.toc = md.toc if match is not None else ''  # 动态给post对象，添加toc属性，然后在模版中处理
    print(post.toc)
        # 如果match为None，说明md转换后的toc属性不匹配正则，说明没有目标，这post.toc赋值为空字符串，然后再模版中处理，非空才渲染
    return render(request, 'blog/detail.html', context={
        'post': post,
    })


# 归档
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={
        'post_list': post_list,
    })


# 分类
def categories(request, category_id):
    category_obj = get_object_or_404(Category, pk=category_id)
    post_list = Post.objects.filter(category=category_obj)
    return render(request, 'blog/index.html', context={
        'post_list': post_list,
    })


# 标签云
def tags(request, tag_id):
    tag_obj = get_object_or_404(Tag, pk=tag_id)
    post_list = Post.objects.filter(tags=tag_obj)
    return render(request, 'blog/index.html', context={
        'post_list': post_list,
    })
