

from django.urls import path
from . import views


app_name = 'blog'   # 定义视图函数、url等的命名空间，模块化管理
from .views import index
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), # path 参数2 接收视图函数类型，
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.PostArchiveView.as_view(), name='archives'),
    path('categories/<int:category_id>/', views.PostCategoryView.as_view(), name='categories'),
    path('tags/<int:tag_id>/', views.PostTagsView.as_view(), name='tags'),
    # path('search/', views.search, name='search'),
    # path('api/index/', views.IndexPostListAPIView.as_view()),
path("api/index/", index),
]