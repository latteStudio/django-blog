

from django.urls import path
from . import views

app_name = 'blog'   # 定义视图函数、url等的命名空间，模块化管理
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    path('categories/<int:category_id>/', views.categories, name='categories'),
    path('tags/<int:tag_id>/', views.tags, name='tags'),

]