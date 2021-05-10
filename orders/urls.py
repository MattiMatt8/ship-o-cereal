from django.urls import path
from . import views

urlpatterns = [
    path("checkout/address/", views.checkout_address, name="checkout_address"),
    path("checkout/address/<int:id>/", views.choose_address, name="choose_address"),
    path("checkout/card/", views.checkout_card, name="checkout_card"),
    path("checkout/card/<int:id>/", views.choose_card, name="choose_card"),
    path("checkout/confirm/", views.checkout_confirm, name="checkout_confirm"),
    path("checkout/finished/", views.checkout_finished, name="checkout_finished"),
]
