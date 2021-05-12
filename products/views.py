from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters.views import FilterView
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from orders.models import OrderItem
from users.models import SearchHistory
from .forms.ProductReviewForm import ProductReviewForm
from .models import Category, Product
from .filters import ProductFilter
import json


class FilteredListView(FilterView):
    """
    A parent class base view for implementing ListView functionality
    with added queryset filtering and pagination maintenance.
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
        search = self.kwargs.get("search_str")
        if search:
            context["page_name"] = f"Search results for {search}"
            context["search_str"] = search
        else:
            category = self.kwargs.get("category_name")
            context["page_name"] = f"All {category}"
        return context


class ProductsInCategoryListView(FilteredListView):
    """
    Class based view for listing and paginating products in a category, either
    all products or products matching query parameters.
    """

    paginate_by = 20  # Display 20 products at a time
    filterset_class = ProductFilter  # Filter to apply
    queryset = Product.objects.all()
    context_object_name = "products"
    template_name = "products/products.html"

    def get_queryset(self):
        """Returns a queryset with products in a category matching given query parameters."""

        category = self.get_category()
        return self.queryset.filter(category=category)

    def get_category(self):
        """Returns category object matching keyword argument 'category_name'."""
        return get_object_or_404(Category, name=self.kwargs.get("category_name"))


class ProductSearchView(FilteredListView):
    """
    Class based view for listing and paginating search results
    plus products matching query parameters.
    """

    paginate_by = 20  # Display 20 products at a time
    filterset_class = ProductFilter  # Filter to apply
    queryset = Product.objects.all()
    context_object_name = "products"
    template_name = "products/products.html"

    def get_queryset(self):
        """Returns a queryset with products that their names contain the searched parameter."""

        search = self.kwargs.get("search_str")

        # Adds the search to the search history if the user is logged in and just did the search
        if len(self.request.GET) == 0 and self.request.user.is_authenticated:
            user_search_history_item = SearchHistory(user=self.request.user, search=search)
            user_search_history_item.save()

        return self.queryset.filter(name__icontains=search)


@ensure_csrf_cookie
def product_details(request, id):
    cart = request.session.get("cart")
    quantity = None
    product = get_object_or_404(Product, pk=id)
    if cart:
        quantity = cart.get(str(id))

    form = None
    users_review = None
    if request.user.is_authenticated:
        try:
            users_review = product.review_set.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            if request.user.order_set.filter(id__in=OrderItem.objects.filter(product_id=id).values_list("order_id")):
                # Creates a review form if the user has purchased the product and has not already made a review on it
                form = ProductReviewForm()

    return render(
        request,
        "products/product_details.html", {
            "product": product,
            "quantity": quantity,
            "form": form,
            "users_review": users_review
        },
    )


@login_required
def add_review(request, id):  # TODO: Fix when reviews popup how they are formatted
    # TODO: Delete button for a review?
    # TODO: Update review ting?
    """Endpoint to post a new review."""
    if request.method == "POST":
        # If the user has made a review or has not already purchased the product
        if request.user.review_set.filter(product_id=id) or not request.user.order_set.filter(
                id__in=OrderItem.objects.filter(product_id=id).values_list("order_id")
        ):
            return JsonResponse({"message": "Error: Operation not allowed."}, status=403)
        body = json.loads(request.body.decode("utf-8"))
        form = ProductReviewForm(data={
            "stars": body.get("stars"),
            "title": body.get("title"),
            "review": body.get("review")
        })
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.user.id
            review.product_id = id
            # review.save()
            return JsonResponse(
                {
                    "message": "Review has been added for the product.",
                    "data": {
                        "id": review.id,
                        "full_name": f"{request.user.first_name} {request.user.last_name}",
                        "profile_image": f"/static/media/{request.user.profile.picture}" if request.user.profile.picture else None,
                        "title": f"{review.title}",
                        "stars": f"{review.stars}",
                        "review": f"{review.review}",
                        "date": review.date
                    }
                }, status=201
            )
        return JsonResponse({"message": "Review not valid."}, status=400)
    return JsonResponse({"message": "Error: Method not supported."}, status=405)


def update_review(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                review = request.user.review_set.get(product_id=id)
                body = json.loads(request.body.decode("utf-8"))
                form = ProductReviewForm(data={
                    "stars": body.get("stars"),
                    "title": body.get("title"),
                    "review": body.get("review")
                }, instance=review)
                form.date = now()
                if form.is_valid():
                    form.date = now()
                    form.save()
                    return JsonResponse({"message": "Updated the review.",
                                         "data": {
                                             "id": review.id,
                                             "full_name": f"{request.user.first_name} {request.user.last_name}",
                                             "profile_image": f"/static/media/{request.user.profile.picture}" if request.user.profile.picture else None,
                                             "title": f"{review.title}",
                                             "stars": f"{review.stars}",
                                             "review": f"{review.review}",
                                             "date": review.date
                                         }
                                         }, status=201)
            except ObjectDoesNotExist:
                return JsonResponse({"message": "Error: Review does not exist."}, status=404)
            return JsonResponse({"message": "Review not valid."}, status=400)
        return JsonResponse({"message": "Error: User not authorized."}, status=401)
    return JsonResponse({"message": "Error: Method not supported."}, status=405)


@login_required
def delete_review(request, id, review_id):
    pass
    # next_query = request.GET.get("next")
    # card = get_object_or_404(request.user.card_set, pk=id)
    # card.delete()
    # return redirect("profile" if next_query is None else next_query)
