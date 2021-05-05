from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from users.forms.UserAddressForm import UserAddressForm
from users.forms.UpdateUserForm import UpdateUserForm
from users.forms.RegisterForm import RegisterForm
from users.models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect("index")  # TODO: Possibly change where it redirects
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
def profile(request): # TODO: Test with no address and no card how it looks like
    if request.method == "POST":
        form = UpdateUserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            profile = request.user.profile
            profile.phone = request.POST["phone"]
            profile.picture = request.POST["picture"]
            profile.save()
    else:
        form = UpdateUserForm(instance=request.user,
                              initial={"phone": request.user.profile.phone, "picture": request.user.profile.picture})
    return render(request, "users/profile.html", {
        "form": form
    })


@login_required
def add_address(request):
    if request.method == "POST":
        form = UserAddressForm(data=request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_id = request.user.id
            address.save()
            return redirect("profile")
    else:
        form = UserAddressForm()
    return render(request, "users/add_address.html", {
        "form": form
    })


@login_required
def update_address(request, id):
    address = get_object_or_404(request.user.address_set, pk=id)
    if request.method == "POST":
        form = UserAddressForm(data=request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserAddressForm(instance=address)
    return render(request, "users/update_address.html", {
        "form": form
    })


@login_required
def delete_address(request, id):
    address = get_object_or_404(request.user.address_set, pk=id)
    address.delete()
    return redirect("profile")


@login_required
def add_card(request):
    if request.method == "POST":
        form = UserAddressForm(data=request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_id = request.user.id
            address.save()
            return redirect("profile")
    else:
        form = UserAddressForm()
    return render(request, "users/add_address.html", {
        "form": form
    })


@login_required
def update_card(request, id):
    pass


@login_required
def delete_card(request, id): #
    pass


def cart(request):
    # TODO: Provide all necessary cart data for user

    return render(request, "users/cart.html")
