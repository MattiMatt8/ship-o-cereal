from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.http import Http404
from .models import Category, Product


def product_category(req, category_name):
    context = {}
    category_name = category_name

    try:
        category = Category.objects.get(name=category_name)
        context["category"] = category

        category_products = Product.objects.filter(category_id=category.id)
        context["products"] = category_products

    except Category.DoesNotExist:
        pass

    return render(req, 'category.html', context)


def product_details(response, id):
    return render(
        response,
        "product_details.html",
        {"product": get_object_or_404(Product, pk=id), "amount_list": range(1,11)},
    )
