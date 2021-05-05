from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Category, Product


class ProductCategory(View):
    def get(self, *args, **kwargs):

        context = {}
        try:

            # category_products = Product.objects.filter(category_id=category.id)
            category = Category.objects.get(name=kwargs["category_name"])
            category_products = category.product_set.all()

            context["category"] = category
            context["products"] = category_products
        except Category.DoesNotExist:
            pass

        return render(self.request, 'category/category.html', context)


def product_details(response, id):
    return render(
        response,
        "product_details.html",
        {"product": get_object_or_404(Product, pk=id), "amount_list": range(1, 11)},
    )
