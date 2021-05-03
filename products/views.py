from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product


def products_all(response):
    return HttpResponse("yes")