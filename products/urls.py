from django.urls import path
from . import views

urlpatterns = [
    path("<str:keyword>", views.ProductSearch.as_view(), name="product-search"),
    path("<int:id>", views.product_details, name="product-details"),
    path(
        "<str:category_name>",
        views.ProductsInCategoryListView.as_view(),
        name="product-category",
    ),
    # path("reviews/new/", views.add_review, name="add_review"),
    # path("reviews/<int:id>/", views.update_review, name="update_review"),
    # path("reviews/<int:id>/delete/", views.delete_review, name="delete_review"),
]
