from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from products.models import Product


def index(response):
    return HttpResponse("yes")

def product_details(response, id):
    return render(response, 'views/product_details.html', {
        'product': get_object_or_404(Product, pk=id)
    })