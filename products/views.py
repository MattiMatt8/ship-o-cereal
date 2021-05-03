from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product


def index(response):
    return HttpResponse("yes")