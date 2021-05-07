from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Brand
from django_filters import FilterSet, ModelMultipleChoiceFilter, ModelChoiceFilter
from .models import Product, Label


class ProductFilter(FilterSet):
    labels = ModelMultipleChoiceFilter(queryset=Label.objects.all())

    brand = ModelChoiceFilter(
        queryset=Brand.objects.all().order_by("name"), empty_label=_("Select brand .."),
        widget=forms.Select(
            attrs={
                "class": "rounded border appearance-none border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-500 text-base w-64 h-9 pl-3 pr-10"
            }
        )
    )

    class Meta:
        model = Product
        fields = ["brand"]
