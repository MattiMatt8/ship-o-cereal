from django.utils.translation import gettext_lazy as _

from .models import Brand, Category
from django_filters import (
    FilterSet,
    ModelMultipleChoiceFilter,
    ModelChoiceFilter,
    NumberFilter,
    OrderingFilter,
    CharFilter,
    UUIDFilter,
)
from .models import Product, Label

# Order by fields
PRODUCT_ORDER_BY_FIELDS = (
    ("price", "Price: Low to High"),
    ("-price", "Price: High to Low"),
    ("name", "Name: A to Z"),
    ("-name", "Name: Z to A"),
    ("-id", "Newest arrivals"),
)


class ProductFilter(FilterSet):
    # Filters
    price = NumberFilter(field_name="price")
    name = CharFilter(field_name="name")
    id = NumberFilter(field_name="newest")
    labels = ModelMultipleChoiceFilter(queryset=Label.objects.all())
    brand = ModelChoiceFilter(
        queryset=Brand.objects.filter(id__in = Product.objects.filter(category_id=Category.objects.get(name="Cereal")).values_list("brand_id")),
        field_name="brand",
        empty_label=_("Select brand .."),
    )

    # Order by filter
    ordering = OrderingFilter(
        label="Sort by", choices=PRODUCT_ORDER_BY_FIELDS, empty_label=_("Order by..")
    )

    class Meta:
        model = Product
        fields = ["price", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["brand"].widget.attrs = {
            "class": "rounded border appearance-none border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500 text-base w-64 h-9 pl-3 pr-10"
        }
        self.form.fields["ordering"].widget.attrs = {
            "class": "rounded border appearance-none border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500 text-base w-42 h-9 pl-3 pr-10"
        }


class ProductSearchFilter(FilterSet):
    class Meta:
        model = Product
        fields = {"name": ["contains"]}
