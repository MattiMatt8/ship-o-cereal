from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.product_details, name="product-details"),
    path(
        "<str:category_name>",
        views.ProductsInCategoryListView.as_view(),
        name="product-category",
    ),
    path("<int:id>/reviews/new/", views.add_review, name="add_review"),
    path("<int:id>/reviews/<int:review_id>/", views.update_review, name="update_review"),
    path("<int:id>/reviews/<int:review_id>/delete/", views.delete_review, name="delete_review"),
]
