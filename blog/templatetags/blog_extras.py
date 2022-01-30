from django import template
from ..models import Post, Category, Tag
# 自定义模版标签

register = template.Library()
# 实例化一个注册器


# 最近文章标签
@register.inclusion_tag('blog/inclusion/_recently_post.html', takes_context=True)
def show_recently_post(context, num=5):
    """
    通过装饰器，把该函数注册为自定义的模版标签，标签就是函数名
    引用得到的标签值，就是函数的返回值
    takes_context参数是指，是否把调用该模版标签的父模版的上下文传入
    :param context:
    :param num:取最近几个文章，可以在标签模版中用参数
    :return:
    """
    return {
        'show_recently_post': Post.objects.all().order_by('-created_time')[:num],
    }


# 归档模版标签
@register.inclusion_tag('blog/inclusion/_archive_post.html', takes_context=True)
def show_archive(context):
    return {
        "show_archive": Post.objects.dates('created_time', 'month', order='DESC'),
    #     将所有post的创建实现取到月份，然后按照月份返回，逆序
    }


# 分类模版标签
@register.inclusion_tag('blog/inclusion/_categories.html', takes_context=True)
def show_categories(context):
    return {
        "show_categories": Category.objects.all(),
    }


# 标签云 模版标签
@register.inclusion_tag('blog/inclusion/_tags.html', takes_context=True)
def show_tags(context):
    return {
        "show_tags": Tag.objects.all(),
    }