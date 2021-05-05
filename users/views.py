from django.shortcuts import render
from users.forms.RegisterForm import RegisterForm

def register(request):
    return render(request, "users/register.html", {
        "form": RegisterForm()
    })

def profile(request):
    # TODO: Provide all necessary user data in the context

    return render(request, "users/profile.html")


def cart(request):
    # TODO: Provide all necessary cart data for user

    return render(request, "users/cart.html")