from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters.views import FilterView
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .filters import ProductFilter, ProductSearchFilter


class FilteredListView(FilterView):
    """
    A parent class implementing ListView functionality with
    added queryset filtering and pagination maintenance.
    """

    def get_queryset(self):
        """Returns a filtered queryset corresponding to query parameters."""

        # Calling FilterView base implementation to get a queryset
        # & initialising a filterset attribute
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)

        return self.filterset.qs.distinct()  # Filtered queryset

    def get_context_data(self, **kwargs):
        """Returns context data with the filtered queryset & current query parameters."""

        # Calling FilterView base implementation first to get a context
        # & adding filterset to context for template rendering
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset

        # Adding filter query parameters to maintain pagination
        filters = ""
        for k, v in context["filterset"].data.items():
            if k != "page":
                filters += f"&{k}={v}"

        context["filters"] = filters
        return context


class ProductsInCategoryListView(FilteredListView):
    """
    A class for listing and paginating products in a category, either
    all products or products matching query parameters.
    """

    paginate_by = 10  # Display 10 products at a time
    filterset_class = ProductFilter  # Filter to apply
    queryset = Product.objects.all()
    context_object_name = "products"
    template_name = "category/category.html"

    def get_queryset(self):
        """Returns a queryset with products in a category matching given query parameters."""

        category = self.get_category()
        return self.queryset.filter(category=category)

    def get_category(self):
        """Returns category object matching keyword argument 'category_name'."""

        return Category.objects.get(name=self.kwargs["category_name"])


class ProductSearch(FilteredListView):
    """
    A class for listing and paginating products based on search paremeters.
    """

    filterset_class = ProductSearchFilter
    template_name = "product_search.html"

    def get(self, request, *args, **kwargs):
        """Method for handling a GET request when searching for products."""

        product_name = request.GET.get("searched")  # The product name provided

        # If product name provided then
        # render template and filter queryset with given product name
        if product_name:
            filterset = self.filterset_class(
                request.GET, queryset=Product.objects.filter(name__icontains=product_name)
            )

            # Render template with products containing given product name
            return render(
                request,
                self.template_name,
                {"searched": product_name, "products": filterset},
            )
        # Product name not provided
        else:
            return render(request, self.template_name, {})


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
