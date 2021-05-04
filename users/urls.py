from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from users.forms.LoginForm import LoginForm

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html", authentication_form=LoginForm,
                                     redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path('register/', views.register, name="register"),
]
