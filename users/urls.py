from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from users.forms.LoginForm import LoginForm

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html", authentication_form=LoginForm,
                                     redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path('register/', views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("profile/cards/new/", views.add_card, name="add_card"),
    path("profile/cards/<int:id>/", views.update_card, name="update_card"),
    path("profile/cards/<int:id>/delete", views.delete_card, name="delete_card"),
    path("profile/addresses/new/", views.add_address, name="add_address"),
    path("profile/addresses/<int:id>/", views.update_address, name="update_address"),
    path("profile/addresses/<int:id>/delete/", views.delete_address, name="delete_address"),
    path("cart/", views.cart, name="cart"),
    path("cart/checkout/address", views.checkout_address, name="checkout_address"),
    path("cart/checkout/card", views.checkout_card, name="checkout_card"),
    path("cart/checkout/confirm", views.checkout_confirm, name="checkout_confirm"),
    path("cart/checkout/finished", views.checkout_finished, name="checkout_finished"),
    path("cart/<int:id>", views.carting, name="carting"),
]
