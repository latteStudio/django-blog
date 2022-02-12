from rest_framework import serializers
from .models import Post, Category, Tag
from django.contrib.auth.models import User
from comments.models import Comments


# class CommentSerializer(serializers.Serializer):
# 类似model.Models form.ModelForm form.Form serializer.Serializer serializer.ModelSerializer
# ModelXX前缀的，都是可以根据定义好的Model中的字段定义，自动选择合适的字段类型/约束
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'id',
                'email',
                'name',
                'text',
                'website'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
                'name'
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
                'name',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
                'username',
        ]


class PostRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    # tags = TagSerializer()
    # 该2个字段，非内置数据类型，需要定义单独的序列化的类的对象，来决定如何序列化
    tags = TagSerializer()
    toc = serializers.CharField()
    body_html = serializers.CharField()

    class Meta:
        model = Post
        fields = [
            'id',
                'title',
                'created_time',
                'excerpt',
                'category',
                'user',
                'views',
                'tags',
                'toc',
                'body_html',
        ]




