from django.urls import path
from . import views

urlpatterns = [
    path("checkout/address/", views.checkout_address, name="checkout_address"),
    path("checkout/card/", views.checkout_card, name="checkout_card"),
    path("checkout/confirm/", views.checkout_confirm, name="checkout_confirm"),
    path("checkout/finished/", views.checkout_finished, name="checkout_finished"),
]