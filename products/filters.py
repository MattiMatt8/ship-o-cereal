from django.utils.translation import gettext_lazy as _

from .models import Brand, Category, ProductLabel
from django_filters import (
    FilterSet,
    ModelMultipleChoiceFilter,
    ModelChoiceFilter,
    NumberFilter,
    OrderingFilter,
    CharFilter,
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


def brands(request):
    """Returns only the brands that are relevant to the items being filtered."""
    category = request.resolver_match.kwargs.get("category_name")
    if category:
        return Brand.objects.filter(
            id__in=Product.objects.filter(
                category_id=Category.objects.get(name=category)
            ).values_list("brand_id")
        )
    search = request.resolver_match.kwargs.get("search_str")
    return Brand.objects.filter(
        id__in=Product.objects.filter(
            name__icontains=search
        ).values_list("brand_id")
    )


def labels(request):
    """Returns on the labels that are relevant to the items being filtered."""
    category = request.resolver_match.kwargs.get("category_name")
    if category:
        return Label.objects.filter(id__in=ProductLabel.objects.filter(
            product_id__in=Product.objects.filter(category_id=Category.objects.get(name=category))).values_list("label_id"))
    search = request.resolver_match.kwargs.get("search_str")
    return Label.objects.filter(id__in=ProductLabel.objects.filter(
        product_id__in=Product.objects.filter(name__icontains=search)).values_list("label_id"))


class ProductFilter(FilterSet):
    # Filters
    price = NumberFilter(field_name="price")
    name = CharFilter(field_name="name")
    id = NumberFilter(field_name="newest")
    labels = ModelMultipleChoiceFilter(queryset=labels, conjoined=True)
    brand = ModelChoiceFilter(
        queryset=brands,
        field_name="brand",
        empty_label=_("Select brand..."),
    )

    # Order by filter
    ordering = OrderingFilter(
        label="Sort by", choices=PRODUCT_ORDER_BY_FIELDS, empty_label=_("Order by...")
    )

    class Meta:
        model = Product
        fields = ["price", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adds classes to the brand dropdown menu to style it.
        self.form.fields["brand"].widget.attrs = {
            "class": "filter-btn appearance-none focus:outline-none   text-base pl-3    border-t w-full py-2 border-gray-300 sm:border sm:rounded"
        }
        # Adds classes to the order dropdown menu to style it.
        self.form.fields["ordering"].widget.attrs = {
            "class": "filter-btn appearance-none focus:outline-none   text-base pl-3    border-t border-b w-full py-2 border-gray-300 sm:border sm:rounded"
        }

