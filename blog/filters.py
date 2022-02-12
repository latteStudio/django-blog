from django_filters import rest_framework as drf_filter
from .models import Post


class PostFilter(drf_filter.FilterSet):
    created_year = drf_filter.NumberFilter(
        field_name='created_time', lookup_expr='year'
    )
    created_month = drf_filter.NumberFilter(
        field_name='created_time', lookup_expr='month'
    )

    class Meta:
        model = Post
        fields = ['category', 'tags', 'created_year', 'created_month']