from django.shortcuts import render
from products.models import Product, Category

def index(request):
    # TODO: Send in a context of top 5 products in cereals, bowls and merch (id, title, price, image)

    # Wack temporary code below...
    # categories = ('Cereal', 'Bowls', 'Merchandise')
    # TODO: Fix this. This is only a temporary solution for the DB changes

    context = {'categories':{}}
    categories = Category.objects.all()
    for category in categories:
        context['categories'][category] = Product.objects.filter(category=category.id).order_by('-total_score')[:5]


    # print(context)
    # context['categories'] = categories

    return render(request, 'views/index.html', context=context)
