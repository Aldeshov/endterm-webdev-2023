from django_filters import rest_framework as filters
from app.models import Post


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    text = filters.CharFilter(lookup_expr='icontains')
    dateOfCreation = filters.DateTimeFilter()

    class Meta:
        model = Post
        fields = ('title', 'text', 'dateOfCreation')
