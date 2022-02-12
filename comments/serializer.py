from rest_framework import serializers
from .models import Comments


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'name',
            'email',
            'website',
            'text',
            'created_time',
            'post'
        ]

        read_only_fields  = [
            'created_time',
        ]
        extra_kwargs = {"post": {"write_only": True}}
