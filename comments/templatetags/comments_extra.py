from django import template
from ..forms import CommentsForm
from ..models import Comments


register = template.Library()


@register.inclusion_tag('comments/inclusions/_show_comments_form.html', takes_context=True)
def show_comments_form(context, post, form=None):
    if form is None:
        form = CommentsForm()
    # 一定要返回一个字典，注意是冒号！把return写到else分支去了！
    return {
            'post': post,
            'form': form
        }


@register.inclusion_tag('comments/inclusions/_show_comments.html', takes_context=True)
def show_comments(context, post):
    comments = post.comments_set.all()
    counter = comments.count()

    # 取到url中的post id，再查询所有相关的comment对象，组成列表，然后返回，
    # 返回的数据，再_show_comments.html中渲染
    return {
        "counter": counter,
        "comments": comments
    }