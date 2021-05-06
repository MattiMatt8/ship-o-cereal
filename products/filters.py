from django import forms
from django_filters import FilterSet, MultipleChoiceFilter, ModelMultipleChoiceFilter
from .models import Product, Label


class ProductFilter(FilterSet):

    labels = ModelMultipleChoiceFilter(queryset=Label.objects.all())

    class Meta:
        model = Product
        fields = ["brand"]

