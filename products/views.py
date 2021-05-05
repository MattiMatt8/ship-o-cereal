from django.shortcuts import render, get_object_or_404
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from django.views.generic import ListView
from .models import Category, Product



class ProductCategory(ListView):
    template_name = "category/category.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["products"] = self.object_list
        return context

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs["category_name"])
        return self.category.product_set.all()





def product_details(response, id):
    return render(
        response,
        "product_details.html",
        {"product": get_object_or_404(Product, pk=id), "amount_list": range(1, 11)},
    )
