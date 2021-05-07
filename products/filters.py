from django.utils.translation import gettext_lazy as _

from .models import Brand
from django_filters import FilterSet, ModelMultipleChoiceFilter, ModelChoiceFilter, NumberFilter, OrderingFilter
from .models import Product, Label


PRODUCT_ORDER_BY_FIELDS = {"price" : "Price"}

class ProductFilter(FilterSet):

    price = NumberFilter(field_name="price")

    ordering = OrderingFilter(
        label="Sort by price",
        fields=PRODUCT_ORDER_BY_FIELDS.keys(),
        field_labels=PRODUCT_ORDER_BY_FIELDS,
        empty_label=_("Order by.."),
    )

    labels = ModelMultipleChoiceFilter(queryset=Label.objects.all())
    brand = ModelChoiceFilter(queryset=Brand.objects.all().order_by("name"), empty_label=_("Select brand .."))

    class Meta:
        model = Product
        # fields =["brand"]
        fields = {'price': ['lt', 'gt']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["brand"].widget.attrs = {"class": "rounded border appearance-none border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500 text-base w-64 h-9 pl-3 pr-10"}
        self.form.fields["ordering"].widget.attrs = {"class": "rounded border appearance-none border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500 text-base w-42 h-9 pl-3 pr-10"}
