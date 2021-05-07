from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters.views import FilterView

from orders.models import OrderItem
from .models import Category, Product
from .filters import ProductFilter


class FilteredListView(FilterView):
    # Calls filters in filters.py
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)

        return self.filterset.qs.distinct()


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        filters = ""

        for k, v in context["filterset"].data.items():
            if k != "page":
                filters += f"&{k}={v}"
        context["filters"] = filters

        return context


class ProductsInCategoryListView(FilteredListView):
    # Calls filtered list view
    paginate_by = 10
    filterset_class = ProductFilter
    queryset = Product.objects.all()
    context_object_name = "products"
    template_name = "category/category.html"

    def get_category(self):
        return Category.objects.get(name=self.kwargs["category_name"])

    def get_queryset(self, **kwargs):
        category = self.get_category()

        return self.queryset \
            .filter(category=category) \



@ensure_csrf_cookie
def product_details(request, id):
    cart = request.session.get("cart")
    quantity = None
    product = get_object_or_404(Product, pk=id)
    if cart:
        quantity = cart.get(str(id))
    return render(
        request,
        "product_details.html",
        {"product": product, "quantity": quantity},
    )
