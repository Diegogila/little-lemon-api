from django_filters import rest_framework as filters
from .models import MenuItem

class MenuItemsFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    ordering = filters.OrderingFilter(fields=(
            ('price', 'price'),
        ),
    )
    category = filters.CharFilter(field_name="category__slug")

    class Meta:
        model = MenuItem
        fields = ['price','category']