from rest_framework import serializers
from .models import Post, Category, Tag
from django.contrib.auth.models import User
from comments.models import Comments

from drf_haystack.serializers import HaystackSerializerMixin
from rest_framework.serializers import CharField
from .utils import Highlighter

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


class PostHaystackSerializer(HaystackSerializerMixin, PostRetrieveSerializer):
    title = HighlightedCharField()
    summary = HighlightedCharField(source="body")

    class Meta(PostRetrieveSerializer.Meta):
        search_fields = ['text']
        fields = {
            'id',
            'title',
            'summary',
            'created_time',
            'excerpt',
            'category',
            'user',
            'views',
        }

class HighlightedCharField(CharField):
    def to_representation(self, value):
        value = super().to_representation(value)
        request = self.context["request"]
        query_v = request.query_params['text'] # 传入的查询参数值，比如?text=md中的md
        highlighter = Highlighter(query_v)
        return highlighter.highlight(value)