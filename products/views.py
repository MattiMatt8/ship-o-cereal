from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Category, Product
from .filters import ProductFilter


class ProductsInCategoryListView(ListView):
    template_name = "category/category.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs["category_name"])
        return category.product_set.all()

#class ProductSearch


def product_details(response, id):
    return render(
        response,
        "product_details.html",
        {"product": get_object_or_404(Product, pk=id), "amount_list": range(1, 11)},
    )
