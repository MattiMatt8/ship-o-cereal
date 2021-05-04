from django.shortcuts import render
from products.models import Category
from django.views import generic


class CategoryList(generic.ListView):
    template_name = 'category_list.html'
    model = Category



def index(request):
    # TODO: Send in a context of top 5 products in cereals, bowls and merch (id, title, price, image)

    # Wack temporary code below...
    # categories = ('Cereal', 'Bowls', 'Merchandise')
    # TODO: Fix this. This is only a temporary solution for the DB changes
    context = {
        'categories': {
            'Cereal', 'Bowls', 'Merchandise'
            # category: Product.objects.filter(category__contains=category)[:5] for category in categories
        }
    }
    # print(context)
    # context['categories'] = categories

    return render(request, 'views/index.html', context=context)
