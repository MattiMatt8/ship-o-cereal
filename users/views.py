from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms.RegisterForm import RegisterForm
from users.models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect("/") # TODO: Possibly change where it redirects
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = Profile(user=user, phone=request.POST["phone"])
            user_profile.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {
        "form": form
    })


@login_required
def profile(request):
    # TODO: Provide all necessary user data in the context

    return render(request, "users/profile.html")


def cart(request):
    # TODO: Provide all necessary cart data for user

    return render(request, "users/cart.html")