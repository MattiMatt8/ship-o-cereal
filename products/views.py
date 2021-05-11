from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters.views import FilterView
from django.shortcuts import render, get_object_or_404, redirect

from orders.models import OrderItem
from users.models import SearchHistory
from .forms.AddReview import AddReview
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

        filters = ""
        for k, v in context["filterset"].data.items():
            if k != "page":
                filters += f"&{k}={v}"

        context["filters"] = filters

        print(context)
        return context


class ProductsInCategoryListView(FilteredListView):
    """
    A class for listing and paginating products in a category, either
    all products or products matching query parameters.
    """

    paginate_by = 20  # Display 20 products at a time
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


class ProductSearchView(FilteredListView):
    """
    A class for listing and paginating products based on search paremeters.
    """

    filterset_class = ProductSearchFilter
    template_name = "product_search.html"

    def get(self, request, *args, **kwargs):
        """Method for handling a GET request when searching for products."""

        # The product name provided
        product_name = request.GET.get("query")
        print(product_name)

        # If product name provided
        # render template and filter queryset with given product name
        if product_name:

            # Get the products containing product name
            filterset = self.filterset_class(request.GET, queryset=Product.objects.filter(name__icontains=product_name))

            # Display 20 products per page
            paginator = Paginator(object_list=filterset.qs, per_page=20)
            page_number = request.GET.get('page')  # Current page
            page_obj = paginator.get_page(page_number)

            # Products accessed in the page_obj
            context = {
                "searched": product_name,
                "paginator": paginator,
                "page_obj": page_obj,
                "is_paginated": True,
                "filters": f"&query={product_name}"
            }

            # Render products to site
            return render(request, self.template_name, context)
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


@login_required
def add_review(request, id):
    # TODO: Maybe display what item is being review at the top?
    if request.user.review_set.filter(product_id=id):
        raise PermissionDenied
    elif not request.user.order_set.filter(
        id__in=OrderItem.objects.filter(product_id=id).values_list("order_id")
    ):
        raise PermissionDenied
    if request.method == "POST":
        form = AddReview(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.user.id
            review.product_id = id
            review.save()
            return redirect("product-details", id=id)
    else:
        form = AddReview()
    return render(request, "products/add_review.html", {"form": form})


@login_required
def update_review(request, id, review_id):
    pass
    # next_query = request.GET.get("next")
    # card = get_object_or_404(request.user.card_set, pk=id)
    # if request.method == "POST":
    #     form = UpdateUserCardForm(data=request.POST, instance=card)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("profile" if next_query is None else next_query)
    # else:
    #     form = UpdateUserCardForm(instance=card)
    # return render(
    #     request, "users/update_card.html", {"form": form, "next_query": next_query}
    # )
    #


@login_required
def delete_review(request, id, review_id):
    pass
    # next_query = request.GET.get("next")
    # card = get_object_or_404(request.user.card_set, pk=id)
    # card.delete()
    # return redirect("profile" if next_query is None else next_query)
