from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from products.models import Product, Category
from django.views.generic import View


class HomePageView(View):
    """
    Renders the top 5 products for each category on the home page.
    """

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        # Context containing each category mapped to the
        # corresponding top 5 products
        context = {"categories": {}, "cart": request.session.get("cart")}
        categories = Category.objects.all()

        # Fetching top 5 products for each category
        for category in categories:
            context["categories"][category] = Product.objects.filter(
                category=category.id, active=True
            ).order_by("-review_calculated")[:10]

        return render(request, "index.html", context=context)


def bad_request(request, exception):
    return render(request, "errors/400.html")


def permission_denied(request, exception):
    return render(request, "errors/403.html")


def page_not_found(request, exception):
    return render(request, "errors/404.html")


def server_error(request):
    return render(request, "errors/500.html")
