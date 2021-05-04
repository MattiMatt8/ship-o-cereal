from django.shortcuts import render, get_object_or_404
from products.models import Product, Category
from django.views.generic import View


class HomePageView(View):
    """
    Renders the top 5 products for each category on the home page.
    """

    def get(self, request, *args, **kwargs):

        # Context containing each category mapped to the
        # corresponding top 5 products
        context = {"categories": {}}
        categories = Category.objects.all()

        # Fetching top 5 products for each category
        for category in categories:
            context["categories"][category] = Product.objects.filter(
                category=category.id
            ).order_by("-total_score")[:5]

        return render(request, "index.html", context=context)
