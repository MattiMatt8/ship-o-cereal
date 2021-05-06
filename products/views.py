from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django_filters.views import FilterView
from .models import Category, Product
from .filters import ProductFilter


class FilteredListView(FilterView):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ProductsInCategoryListView(FilteredListView):
    paginate_by = 10
    filterset_class = ProductFilter
    context_object_name = "products"
    template_name = "category/category.html"

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs["category_name"])
        return category.product_set.all()


def product_details(response, id):
    return render(
        response,
        "product_details.html",
        {"product": get_object_or_404(Product, pk=id), "amount_list": range(1, 11)},
    )
