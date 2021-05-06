from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from users.forms.ProfileForm import ProfileForm
from users.forms.UserAddressForm import UserAddressForm
from users.forms.UpdateUserForm import UpdateUserForm
from users.forms.RegisterForm import RegisterForm
from users.forms.AddUserCardForm import AddUserCardForm
from users.forms.UpdateUserCardForm import UpdateUserCardForm
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

#
# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = UpdateUserForm(data=request.POST, files=request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             profile = request.user.profile
#             profile.phone = request.POST["phone"]
#             print("FILES",request.FILES)
#             print("PIC",request.POST["picture"])
#             profile.picture = request.POST["picture"]
#             profile.save()
#     else:
#         form = UpdateUserForm(instance=request.user,
#                               initial={"phone": request.user.profile.phone, "picture": request.user.profile.picture})
#     return render(request, "users/profile.html", {
#         "form": form
#     })


@login_required
def profile(request):
    if request.method == "POST":
        form = UpdateUserForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            profile_form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
            profile_form.save()
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
def add_card(request): # TODO: Possibly fix that card number can't be letters
    if request.method == "POST":
        form = AddUserCardForm(data=request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user_id = request.user.id
            card.save()
            return redirect("profile")
    else:
        form = AddUserCardForm()
    return render(request, "users/add_card.html", {
        "form": form
    })


@login_required
def update_card(request, id):
    card = get_object_or_404(request.user.card_set, pk=id)
    if request.method == "POST":
        form = UpdateUserCardForm(data=request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UpdateUserCardForm(instance=card)
    return render(request, "users/update_card.html", {
        "form": form
    })


@login_required
def delete_card(request, id):
    card = get_object_or_404(request.user.card_set, pk=id)
    card.delete()
    return redirect("profile")


def cart(request):
    # TODO: Provide all necessary cart data for user

    return render(request, "users/cart.html")


# TODO: Check if these should exist in another app, maybe a cart app? idk bro

def checkout_address(request):
    pass

def checkout_card(request):
    pass

def checkout_confirm(request):
    pass