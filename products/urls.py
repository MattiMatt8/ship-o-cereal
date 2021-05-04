from django.urls import path
from . import views

urlpatterns = [
    path("cereal", views.index, name="cereals-index"),
    path("<int:id>", views.product_details, name="product-details"),
]