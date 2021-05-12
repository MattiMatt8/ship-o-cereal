from fractions import Fraction

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, DetailView

from ShipOCereal import settings
from orders.models import OrderItem, Order
from orders.views import get_order, keep_order
from products.models import Product
from users.forms.AddSearchHistoryForm import AddSearchHistoryForm
from users.forms.ProfileForm import ProfileForm
from users.forms.UserAddressForm import UserAddressForm
from users.forms.UpdateUserForm import UpdateUserForm
from users.forms.RegisterForm import RegisterForm
from users.forms.AddUserCardForm import AddUserCardForm
from users.forms.UpdateUserCardForm import UpdateUserCardForm
from users.models import Profile
import json


class OrdersListView(ListView):
    """A view for displaying a list of orders for a given user"""

    model = Order
    template_name = "profile/order_history/orders.html"

    def get_context_data(self):
        """Returns the context for this view. Context containing the orders for a given user"""

        orders = self.request.user.order_set.all()  # match orders by user in request
        return {"order_history": orders}


class OrderDetailView(DetailView):
    """A view for displaying details of a order for a given user"""

    model = Order
    template_name = "profile/order_history/order_details.html"

    def get_context_data(self):
        """
        Returns the context for this view. Context containing the products and details of a
        specific order for a given order
        """

        # Get an order matching a given order_id sent by a user
        order = get_object_or_404(self.request.user.order_set, pk=self.kwargs['pk'])
        order_items = OrderItem.objects.filter(order_id=order.id)  # Get the order items for the order

        context = {"order": order, "order_items": order_items}
        return context


def register(request):
    '''View for registering a new user.'''
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        # Registers the account if it's valid
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = Profile(user=user, phone=request.POST["phone"])
            user_profile.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    '''View for the users profile.'''
    if request.method == "POST":
        # Updates the users profile if it's valid
        form = UpdateUserForm(
            data=request.POST, files=request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            profile_form = ProfileForm(
                data=request.POST, files=request.FILES, instance=request.user.profile
            )
            profile_form.save()
    else:
        # Creates a form with the users current information
        form = UpdateUserForm(
            instance=request.user,
            initial={
                "phone": request.user.profile.phone,
                "picture": request.user.profile.picture,
            },
        )
    return render(request, "profile/profile.html", {"form": form})


@login_required
def add_address(request):
    '''View for adding a new address to the user.'''
    # Gets the query if the user should be redirected to a different page
    next_query = request.GET.get("next")

    if request.method == "POST":
        # Creates the address for the user if it's valid
        form = UserAddressForm(data=request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_id = request.user.id
            address.save()
            if next_query:
                # Sends the user to a custom page
                return redirect(f"{next_query}?select={address.id}")
            return redirect("profile")
    else:
        form = UserAddressForm()
    return render(request, "users/add_address.html", {"form": form})


@login_required
def update_address(request, id):
    """View to update users address."""
    next_query = request.GET.get("next")
    address = get_object_or_404(request.user.address_set, pk=id)
    if request.method == "POST":
        # Updates the users address if it's valid
        form = UserAddressForm(data=request.POST, instance=address)
        if form.is_valid():
            form.save()
            # Sends the user to his profile or a custom page
            return redirect("profile" if next_query is None else next_query)
    else:
        form = UserAddressForm(instance=address)
    return render(
        request, "users/update_address.html", {"form": form, "next_query": next_query}
    )


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
            if next_query:
                return redirect(f"{next_query}?select={card.id}")
            return redirect("profile")
    else:
        form = AddUserCardForm()
    return render(request, "users/add_card.html", {"form": form})


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
    return render(
        request, "users/update_card.html", {"form": form, "next_query": next_query}
    )


@login_required
def delete_card(request, id):
    next_query = request.GET.get("next")
    card = get_object_or_404(request.user.card_set, pk=id)
    card.delete()
    return redirect("profile" if next_query is None else next_query)


def update_cart(request, id):
    if request.method == "POST":
        cart_total = request.session.get("cart_total")
        body = json.loads(request.body.decode("utf-8"))
        in_cart = body.get("in_cart")
        quantity = body.get("quantity")
        cart = request.session.get("cart")
        str_id = str(id)
        if not cart or not isinstance(cart, dict):
            cart = dict()
            request.session["cart"] = cart
            request.session["cart_total"] = 0
            cart_total = 0
        old_quantity = cart.get(str_id)
        if (
                cart_total + quantity - (old_quantity if old_quantity else 0)
        ) > settings.MAX_ITEMS_IN_CART:
            return JsonResponse({"message": "Cart item amount exceeded."}, status=400)
        if old_quantity:
            request.session["cart_total"] -= old_quantity
        cart[str_id] = quantity
        if in_cart:
            order_items = []
            for obj in serializers.deserialize(
                    "json", request.session.get("order_items")
            ):
                order_item = obj.object
                if order_item.product.id == id:
                    order_item.quantity = quantity
                order_items.append(order_item)
            request.session["order_items"] = serializers.serialize("json", order_items)
        request.session.modified = True
        request.session["cart_total"] += quantity
        return JsonResponse(
            {"message": "Cart updated.", "old_quantity": old_quantity}, status=201
        )
    return JsonResponse({"message": "Error: Method not supported."}, status=405)


def delete_from_cart(request, id):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            in_cart = body.get("in_cart")
            quantity = request.session["cart"][str(id)]
            del request.session["cart"][str(id)]
            request.session.modified = True
            request.session["cart_total"] -= quantity
            if in_cart:
                order_items = []
                for obj in serializers.deserialize(
                        "json", request.session.get("order_items")
                ):
                    order_item = obj.object
                    if order_item.product.id != id:
                        order_items.append(order_item)
                request.session["order_items"] = serializers.serialize(
                    "json", order_items
                )
            return JsonResponse(
                {"message": "Item deleted from cart.", "quantity": quantity}, status=200
            )
        except KeyError:
            return JsonResponse({"message": "Error: Item does not exist."}, status=404)


def cart_amount(request):
    cart = request.session.get("cart")
    products_amount_fraction = Fraction()
    if cart:
        for obj in serializers.deserialize("json", request.session.get("order_items")):
            order_item = obj.object
            products_amount_fraction += (
                    Fraction.from_float(order_item.price) * order_item.quantity
            )
    products_amount = round(float(products_amount_fraction), 2)
    shipping_amount = 0 if products_amount > 20 else settings.DEFAULT_SHIPPING_AMOUNT
    total_amount = round(float(products_amount_fraction + Fraction(shipping_amount)), 2)
    if products_amount != 0:
        order = get_order(request)
        order.total = total_amount
        order.shipping_cost = shipping_amount
        order.products_total = products_amount
        keep_order(request, order)
    return JsonResponse(
        {
            "data": {
                "products_amount": products_amount,
                "shipping_amount": shipping_amount,
                "total_amount": total_amount,
            }
        },
        status=200,
    )


@ensure_csrf_cookie
def cart(request):
    cart = request.session.get("cart")
    cart_total = 0
    updated_cart = {}
    order_items = []
    products_amount_fraction = Fraction()
    order = get_order(request)
    if order is None:
        order = Order()
    if cart:
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(pk=int(product_id))
                price = product.discounted_price if product.discounted_price else product.price
                order_items.append(
                    OrderItem(quantity=quantity, product=product,
                              price=price)
                )
                cart_total += quantity
                products_amount_fraction += (
                        Fraction.from_float(price) * quantity
                )
                updated_cart[product_id] = quantity
            except ObjectDoesNotExist:
                pass
        request.session["cart_total"] = cart_total
    request.session["cart"] = updated_cart
    order.products_total = round(float(products_amount_fraction), 2)
    order.shipping_cost = (
        0 if order.products_total > 20 else settings.DEFAULT_SHIPPING_AMOUNT
    )
    order.total = round(
        float(products_amount_fraction + Fraction(order.shipping_cost)), 2
    )
    if len(order_items) > 0:
        keep_order(request, order)
        request.session["order_items"] = serializers.serialize("json", order_items)

    else:
        order_items = None
    return render(
        request, "users/cart.html", {"order": order, "order_items": order_items}
    )


def new_search(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            body = json.loads(request.body.decode("utf-8"))
            form = AddSearchHistoryForm(data={"search": body.get("search")})
            if form.is_valid():
                form.save(commit=False)
                form.user_id = request.user.id
                form.save()
                return JsonResponse({"message": "Added to users search history."}, status=201)
            return JsonResponse({"message": "Search not valid."}, status=400)
        return JsonResponse({"message": "Error: User not authorized."}, status=401)
    return JsonResponse({"message": "Error: Method not supported."}, status=405)


def delete_search(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                search_history = request.user.searchhistory_set.get(pk=id)
                search_history.delete()
                return JsonResponse({"message": "Deleted from users search history."}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({"message": "Error: Item does not exist."}, status=404)
        return JsonResponse({"message": "Error: User not authorized."}, status=401)
    return JsonResponse({"message": "Error: Method not supported."}, status=405)
