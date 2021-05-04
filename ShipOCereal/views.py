from django.shortcuts import render
from products.models import Product

def index(request):
    # TODO: Send in a context of top 5 products in cereals, bowls and merch (id, title, price, image)

    # Wack temporary code below...
    categories = ('Cereal', 'Bowls', 'Merchandise')
    context = {
        'categories': {
            category: Product.objects.filter(category__contains=category)[:5] for category in categories
        }
    }
    print(context)
    #context['categories'] = categories

    return render(request, 'views/index.html', context=context)
