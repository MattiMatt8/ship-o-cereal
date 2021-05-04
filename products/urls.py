from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="products-index"),
    path('<int:id>', views.product_details, name="product-details")
]