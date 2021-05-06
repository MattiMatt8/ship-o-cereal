from django_filters import FilterSet, ChoiceFilter
from .models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = ["brand"]

