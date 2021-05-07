from fractions import Fraction

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from orders.models import OrderItem
from products.models import Product
from users.forms.ProfileForm import ProfileForm
from users.forms.UserAddressForm import UserAddressForm
from users.forms.UpdateUserForm import UpdateUserForm
from users.forms.RegisterForm import RegisterForm
from users.forms.AddUserCardForm import AddUserCardForm
from users.forms.UpdateUserCardForm import UpdateUserCardForm
from users.models import Profile
import json


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


def update_cart_total(request, id, quantity, update=False):
    cart_total = request.session.get("cart_total")
    if update:
        request.session["cart_total"] -= request.session["cart"][id]
    request.session["cart_total"] += quantity


def cart_help(request, id, update=False):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        quantity = body.get("quantity")
        cart = request.session.get("cart")
        str_id = str(id)
        old_quantity = 0
        if not cart or not isinstance(cart, dict):
            cart = dict()
            request.session["cart"] = cart
            request.session["cart_total"] = 0
        if cart.get(str_id) and not update:
            cart[str_id] += quantity
            request.session.modified = True
            request.session["cart_total"] += quantity
        else:
            if cart.get(str_id):
                old_quantity = request.session["cart"][str_id]
                request.session["cart_total"] -= old_quantity
            cart[str_id] = quantity
            request.session.modified = True
            request.session["cart_total"] += quantity
        return JsonResponse({"message": "Cart updated.", "old_quantity": old_quantity})
    return JsonResponse({"message": "Error: Method not supported."})


def add_to_cart(request, id):
    return cart_help(request, id)


def update_cart(request, id):
    return cart_help(request, id, True)


def delete_from_cart(request, id):
    if request.method == "POST":
        try:
            quantity = request.session["cart"][str(id)]
            del request.session["cart"][str(id)]
            request.session.modified = True
            request.session["cart_total"] -= quantity
            return JsonResponse({"message": "Item deleted from cart.", "quantity": quantity})
        except KeyError:
            return JsonResponse({"message": "Error: Item does not exist."})


def cart_amount(request):
    cart = request.session.get("cart")
    products_amount_fraction = Fraction()
    if cart:
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(pk=int(product_id))
                products_amount_fraction += Fraction.from_float(product.price) * quantity
            except ObjectDoesNotExist:
                pass
    else:
        products = None
    products_amount = float(products_amount_fraction)
    shipping_amount = 0 if products_amount > 20 else 10
    total_amount = float(products_amount_fraction + Fraction(shipping_amount))
    return JsonResponse({
        "products_amount": products_amount,
        "shipping_amount": shipping_amount,
        "total_amount": total_amount
    })


@ensure_csrf_cookie
def cart(request):
    # TODO: Provide all necessary cart data for user
    cart = request.session.get("cart")
    cart_total = 0
    products = []
    products_amount_fraction = Fraction()
    if cart:
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(pk=int(product_id))
                products.append(OrderItem(quantity=quantity, product=product, price=product.price))
                cart_total += quantity
                products_amount_fraction += Fraction.from_float(product.price) * quantity
            except ObjectDoesNotExist:
                pass
        request.session["cart_total"] = cart_total
    else:
        products = None
    products_amount = float(products_amount_fraction)
    shipping_amount = 0 if products_amount > 20 else 10
    total_amount = float(products_amount_fraction + Fraction(shipping_amount))
    return render(request, "users/cart.html", {
        "products": products if len(products) > 0 else None,
        "products_amount": products_amount,
        "shipping_amount": shipping_amount,
        "total_amount": total_amount
    })


# TODO: Check if these should exist in another app, maybe a cart app? idk bro
@login_required
def checkout_address(request): # TODO: Make sure cart is not empty
    return render(request, "orders/checkout_address.html")

@login_required
def checkout_card(request): # TODO: Make sure address has been selected
    return render(request, "orders/checkout_card.html")


@login_required
def checkout_confirm(request): # TODO: Make sure address and card have been selected
    return render(request, "orders/checkout_confirm.html")

def checkout_finished(request):
    return render(request, "orders/checkout_finished.html")

