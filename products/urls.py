from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_all, name="products_all"),
]