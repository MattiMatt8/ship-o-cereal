from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name = "views/users/login.html"), name="user_login"),
    # path('register/', views.login, name="user_register"),
]