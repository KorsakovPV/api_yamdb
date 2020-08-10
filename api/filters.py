from django_filters import rest_framework as filters

from content.models import Title


class TitleFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='exact')
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    year = filters.NumberFilter(field_name='year', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
