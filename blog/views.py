from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
# Create your views here.

from .models import Post, Category, Tag
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from pure_pagination import PaginationMixin
# 通用视图改造
from django.views.generic import ListView, DetailView
# 分别使用于：某个对象集合的列表页；某个对象的详情页
# 代码逻辑类似，可抽取：
# 对某个对象-》某个表，查询所有对象，返回列表集合，集合模版渲染：列表页
    # 非所有对象，有过滤条件，比如：博客按分类查询、日期归档查询、标签查询（有过滤条件）
# 根据某条件，比如pk，查询到具体的对象，然后返回对象具体数据，结合模版渲染，详情页

from django.db.models import Q


# rest-api 相关导入
from rest_framework import status
from .serializers import PostRetrieveSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')   # -为逆序排序
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list,
#     })


# def search(request):
#     value = request.GET.get('q')
#     post_list = Post.objects.all().filter(Q(title__icontains=value) | Q(body__icontains=value))
#
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list,
#     })


class IndexView(PaginationMixin, ListView):
    model = Post    # 查那个模型-表？
    template_name = 'blog/index.html'   # 渲染模版是？
    context_object_name = 'post_list'   # 定义给模版中引用的变量，其值应该是查询后的所有对象的列表
    paginate_by = 10 # 每10个分一页

# # 首页视图——rest改进
# @api_view(http_method_names=['GET'])    #   装饰后，index视图函数就成了restful api的视图，装饰器内部实现了：内容协商、认证、鉴权、限流等
# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     serializer = PostListSerializer(post_list, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny

# # 首页列表，用rest-api的类视图改进：
# class IndexPostListAPIView(ListAPIView):
#     """逻辑通用，在继承的ListAPIView继承中实现，只需定义返回哪个查询的结果集
#         结果集中对象，如何序列化
#         如何分页
#         访问的权限
#     """
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     pagination_class = PageNumberPagination
#     permission_classes = [AllowAny]


# 首页列表，用视图集改进，一个对象的所有支持方法，对应的视图函数，用视图集定义
from rest_framework import viewsets
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.serializers import DateField, CharField

from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter
from comments.serializer import CommentsSerializer

from drf_haystack.viewsets import HaystackViewSet
from .serializers import PostHaystackSerializer

from .utils import Highlighter
# 导入自定义的改过的高亮类


from  rest_framework_extensions.cache.decorators import cache_response


class PostSearchView(HaystackViewSet):
    index_models = [Post]
    serializer_class = PostHaystackSerializer


from rest_framework_extensions.key_constructor.bits import (
    ListSqlQueryKeyBit,
    PaginationKeyBit,
    RetrieveSqlQueryKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from .utils import UpdatedAtKeyBit


class PostUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "post_updated_at"


class CommentUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "comment_updated_at"


class PostListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = PostUpdatedAtKeyBit()


class PostObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = PostUpdatedAtKeyBit()


class CommentListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = CommentUpdatedAtKeyBit()


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = PostRetrieveSerializer
    queryset = Post.objects.all()
    # pagination_class = PageNumberPagination
    pagination_class = LimitOffsetPagination
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend]
    filter_class = PostFilter

    @cache_response(timeout=5*60, key_func=PostListKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(timeout=5*60, key_func=PostObjectKeyConstructor())
    def retrieve(self, request, *args, **kwargs):
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='archive/dates', url_name='archive-date')
    def list_archive_dates(self, request, *args, **kwargs):
        dates = Post.objects.dates('created_time', 'month', order='DESC')
        date_field = DateField()
        data = [date_field.to_representation(date) for date in dates]
        return Response(data=data, status=status.HTTP_200_OK)

    @cache_response(timeout=5*60, key_func=CommentListKeyConstructor())
    @action(methods=['GET'], detail=True, url_path='comments', url_name='comment', pagination_class=LimitOffsetPagination, serializer_class=CommentsSerializer)
    def list_comments(self, request, *args, **kwargs):
        post = self.get_object()
        queryset = post.comments_set.all().order_by('-created_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

index = PostViewSet.as_view({'get': 'list'})

# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     # 阅读量+1
#     post.update_views()
#
#     md = markdown.Markdown(extensions=[   # 将数据库中存储的markdown格式的文本，经由markdown库转为html格式，然后再结合模版渲染！
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#         TocExtension(slugify=slugify),
#     ])
#     post.body = md.convert(post.body)   # 对post的body进行转换
#
#     match = re.search(r'<div class="toc">\s*<ul>(.+)</ul>\s*</div>', md.toc, re.S)
#
#     post.toc = md.toc if match is not None else ''  # 动态给post对象，添加toc属性，然后在模版中处理
#     print(post.toc)
#         # 如果match为None，说明md转换后的toc属性不匹配正则，说明没有目标，这post.toc赋值为空字符串，然后再模版中处理，非空才渲染
#     return render(request, 'blog/detail.html', context={
#         'post': post,
#     })


class PostDetailView(DetailView):
    model = Post    # 查哪个模型-表？
    template_name = 'blog/detail.html'   # 定义渲染模版
    context_object_name = 'post'   # 定义给模版中引用的变量，其值应该是查询后的所有对象的列表

    def get(self, request, *args, **kwargs):

        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.update_views() # 父类的get，得到相应的Post实例，赋值给self.object属性，然后调用访问量+1方法
        return response

#     # 会get方法调用，
#     def get_object(self, queryset=None):
# #         重写该方法为了：实现和视图函数中md格式渲染
#         post = super().get_object(queryset=None)
#         # 父类的方法，返回相应的实例，-》到get方法中，又包装了一层，赋值给了object属性
#         md = markdown.Markdown(extensions=[   # 将数据库中存储的markdown格式的文本，经由markdown库转为html格式，然后再结合模版渲染！
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',
#             'markdown.extensions.toc',
#             TocExtension(slugify=slugify),
#         ])
#         post.body = md.convert(post.body)   # 对post的body进行转换
#
#         match = re.search(r'<div class="toc">\s*<ul>(.+)</ul>\s*</div>', md.toc, re.S)
#
#         post.toc = md.toc if match is not None else ''  # 动态给post对象，添加toc属性，然后在模版中处理
#         return post



# 归档
# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list,
#     })


class PostArchiveView(IndexView):
    # 这里可以继承IndexView，因为针对同一个对象，模版、模版变量相同
    # 然后重写父类的query_set()方法，默认是返回所有post对象，但归档需要根据日期进行过滤
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(PostArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


# 分类
# def categories(request, category_id):
#     category_obj = get_object_or_404(Category, pk=category_id)
#     post_list = Post.objects.filter(category=category_obj)
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list,
#     })


class PostCategoryView(IndexView):
    """
    分类和标签云，查询的对象，使用的模版，都是一样的
        所以，可继承自IndexView
    唯一不同的是：
        覆盖父类的get_queryset,父类的该方法，默认返回所有post对象，所以先根据url中捕获的命名分组，在分类或标签表中
        根据捕获的pk主键，查到相应的对象，
        然后调用父类的get_queryset再根据分类或标签对象，作为过滤条件，得到过滤后的集合，并返回
    """
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        return super(PostCategoryView, self).get_queryset().filter(category=cate)


# 标签云
# def tags(request, tag_id):
#     tag_obj = get_object_or_404(Tag, pk=tag_id)
#     post_list = Post.objects.filter(tags=tag_obj)
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list,
#     })


class PostTagsView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('tag_id'))
        return super(PostTagsView, self).get_queryset().filter(tags=tag)


