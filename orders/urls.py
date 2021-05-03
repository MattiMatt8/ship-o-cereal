from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_orders, name="all_orders"),
]