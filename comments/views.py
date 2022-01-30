from django.shortcuts import render, get_object_or_404, redirect
from .models import Comments
# Create your views here.
from .forms import CommentsForm
from django.views.decorators.http import require_POST
from blog.models import Post
from django.contrib import messages


@require_POST   #只允许post方法能访问
def comments(request, post_pk):
    form_obj = CommentsForm(request.POST)
#     从客户端传来的数据中，实例化得到一个form
    print(request.POST)
    print(form_obj)

    post = get_object_or_404(Post, pk=post_pk)
#     查到提交的评论对应post实例

#     如果表单数据全部合法，先在内存中生成对应的Comment的实例，再把post关联掉，最后保存到数据库，然后重新返回提交后的该对应post的详情页，重新渲染！
    if form_obj.is_valid():
        comment = form_obj.save(commit=False)
        comment.post = post
        comment.save()

        messages.add_message(request, messages.SUCCESS, "评论发表成功!", extra_tags="success")
        return redirect(post)
#             会自动调用post所在类即Post的get_absolute_url方法，可以实现返回原url

#     如果表单不合法，就渲染一个错误页面（该页面携带了客户刚提交错的表单数据，用于提示修改
    messages.add_message(request, messages.ERROR, "评论发表失败!请修改表单中错误项后再提交", extra_tags="danger")
    return render(request, 'comments/preview.html', context={
        "post": post,
        "form": form_obj,
    })