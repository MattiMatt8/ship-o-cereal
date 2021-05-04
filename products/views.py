from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse
from .models import Category, Product

class CategoryListView(View):
    model = Category


def index(response):
    return HttpResponse("yes")


def product_details(response, id):
    return render(
        response,
        "views/product_details.html",
        {"product": get_object_or_404(Product, pk=id)},
    )
