from fractions import Fraction

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from ShipOCereal import settings
from orders.models import OrderItem, Order
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
    next_query = request.GET.get("next")
    if request.method == "POST":
        form = UserAddressForm(data=request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_id = request.user.id
            address.save()
            if (next_query):
                request.session["checkout_address_id"] = address.id
                return redirect(next_query)
            return redirect("profile")
    else:
        form = UserAddressForm()
    return render(request, "users/add_address.html", {
        "form": form
    })


@login_required
def update_address(request, id):
    next_query = request.GET.get("next")
    address = get_object_or_404(request.user.address_set, pk=id)
    if request.method == "POST":
        form = UserAddressForm(data=request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect("profile" if next_query is None else next_query)
    else:
        form = UserAddressForm(instance=address)
    return render(request, "users/update_address.html", {
        "form": form,
        "next_query": next_query
    })


@login_required
def delete_address(request, id):
    next_query = request.GET.get("next")
    address = get_object_or_404(request.user.address_set, pk=id)
    address.delete()
    return redirect("profile" if next_query is None else next_query)


@login_required
def add_card(request):
    next_query = request.GET.get("next")
    if request.method == "POST":
        form = AddUserCardForm(data=request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user_id = request.user.id
            card.save()
            if (next_query):
                request.session["checkout_card_id"] = card.id
                return redirect(next_query)
            return redirect("profile")
    else:
        form = AddUserCardForm()
    return render(request, "users/add_card.html", {
        "form": form
    })


@login_required
def update_card(request, id):
    next_query = request.GET.get("next")
    card = get_object_or_404(request.user.card_set, pk=id)
    if request.method == "POST":
        form = UpdateUserCardForm(data=request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect("profile" if next_query is None else next_query)
    else:
        form = UpdateUserCardForm(instance=card)
    return render(request, "users/update_card.html", {
        "form": form,
        "next_query": next_query
    })


@login_required
def delete_card(request, id):
    next_query = request.GET.get("next")
    card = get_object_or_404(request.user.card_set, pk=id)
    card.delete()
    return redirect("profile" if next_query is None else next_query)


def cart_help(request, id):
    if request.method == "POST":
        cart_total = request.session.get("cart_total")
        body = json.loads(request.body.decode('utf-8'))
        quantity = body.get("quantity")
        cart = request.session.get("cart")
        str_id = str(id)
        if not cart or not isinstance(cart, dict):
            cart = dict()
            request.session["cart"] = cart
            request.session["cart_total"] = 0
            cart_total = 0
        old_quantity = cart.get(str_id)
        if (cart_total + quantity - (old_quantity if old_quantity else 0)) > 100:
            return JsonResponse({"message": "Error: Cart item amount exceeded."}, status=400)
        if old_quantity:
            request.session["cart_total"] -= old_quantity
        cart[str_id] = quantity
        request.session.modified = True
        request.session["cart_total"] += quantity
        return JsonResponse({"message": "Cart updated.", "old_quantity": old_quantity}, status=201)
    return JsonResponse({"message": "Error: Method not supported."}, status=405)


def update_cart(request, id):
    return cart_help(request, id)


def delete_from_cart(request, id):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode('utf-8'))
            in_cart = body.get("in_cart")
            quantity = request.session["cart"][str(id)]
            del request.session["cart"][str(id)]
            request.session.modified = True
            request.session["cart_total"] -= quantity

            if in_cart:
                order_items = []
                print(request.session.get("order_items"))
                for obj in serializers.deserialize("json", request.session.get("order_items")):
                    order_item = obj.object
                    if order_item.product.id != id:
                        order_items.append(order_item)
                request.session["order_items"] = serializers.serialize("json", order_items)

                print(request.session.get("order_items"))
            return JsonResponse({"message": "Item deleted from cart.", "quantity": quantity}, status=200)
        except KeyError:
            return JsonResponse({"message": "Error: Item does not exist."}, status=405)


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
    products_amount = round(float(products_amount_fraction), 2)
    shipping_amount = 0 if products_amount > 20 else settings.DEFAULT_SHIPPING_AMOUNT
    total_amount = round(float(products_amount_fraction + Fraction(shipping_amount)), 2)
    if products_amount != 0:
        for obj in serializers.deserialize("json", request.session.get("order")):
            order = obj.object
        order.total = total_amount
        order.shipping_cost = shipping_amount
        order.products_total = products_amount
        request.session["order"] = serializers.serialize("json", [order])
    return JsonResponse({
        "data": {
            "products_amount": products_amount,
            "shipping_amount": shipping_amount,
            "total_amount": total_amount
        }
    }, status=200)

# TODO: While in cart make it so that if amount is changed or item delete it changes the OrderItem which
# TODO: will be stored a session
@ensure_csrf_cookie
def cart(request):
    cart = request.session.get("cart")
    cart_total = 0
    updated_cart = {}
    order_items = []
    products_amount_fraction = Fraction()
    order = Order()
    if cart:
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(pk=int(product_id))
                order_items.append(OrderItem(quantity=quantity, product=product, price=product.price))
                cart_total += quantity
                products_amount_fraction += Fraction.from_float(product.price) * quantity
                updated_cart[product_id] = quantity
            except ObjectDoesNotExist:
                pass
        request.session["cart_total"] = cart_total
    request.session["cart"] = updated_cart
    order.products_amount = round(float(products_amount_fraction),2)
    order.shipping_cost = 0 if order.products_amount > 20 else settings.DEFAULT_SHIPPING_AMOUNT
    order.total = round(float(products_amount_fraction + Fraction(order.shipping_cost)),2)
    if len(order_items) > 0:
        request.session["order"] = serializers.serialize("json", [order])
        request.session["order_items"] = serializers.serialize("json", order_items)
        print(request.session["order_items"]) # TODO: REMOVE
        # for order_item in serializers.deserialize("json", request.session.get("order_items")):
        #     order_item.save()
    else:
        order_items = None
    return render(request, "users/cart.html", {
        "order": order,
        "order_items": order_items
    })
