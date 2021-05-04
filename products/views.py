from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse
from .models import Category, Product


def product_category(req, category_name):
    category_name = category_name.lower().capitalize()
    category = get_object_or_404(Category, name=category_name)
    return render(req, 'category.html', {"category": category})


def product_details(response, id):
    return render(
        response,
        "product_details.html",
        {"product": get_object_or_404(Product, pk=id), "amount_list": range(1,11)},
    )
