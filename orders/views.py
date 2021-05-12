from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.utils.timezone import now

from orders.models import Status


@login_required
def checkout_address(request):
    error_message = None
    order = get_order(request)
    cart = request.session.get("cart")
    if order is None or cart is None or len(cart) == 0:
        raise PermissionDenied
    if request.method == "POST":
        try:
            address = request.user.address_set.get(pk=request.POST.get("address"))
            order.address_street_name = address.street_name
            order.address_house_number = address.house_number
            order.address_city = address.city
            order.address_zip = address.zip
            order.address_country = address.country
            order.address_additional_comments = address.additional_comments
            keep_order(request, order)
            return redirect("checkout_card")
        except ObjectDoesNotExist:
            error_message = "Invalid address."
    select = request.GET.get("select")
    select_address = None
    if select:
        try:
            select_address = int(select)
        except ValueError:
            pass
    return render(
        request,
        "orders/checkout_address.html",
        {"error_message": error_message, "select_address": select_address},
    )


@login_required
def checkout_card(request):
    error_message = None
    order = get_order(request)
    cart = request.session.get("cart")
    if order is None or order.address_zip is None or cart is None or len(cart) == 0:
        raise PermissionDenied
    if request.method == "POST":
        cvc = request.POST.get("CVCfield")
        try:
            card = request.user.card_set.get(pk=request.POST.get("card"))
            cvc_int = int(cvc)
            if len(cvc) != 3:
                raise ValueError
            request.session["checkout_card"] = serializers.serialize("json", [card])
            request.session["checkout_cvc"] = cvc_int
            return redirect("checkout_confirm")
        except ValueError:
            error_message = "Invalid CVC number."
        except ObjectDoesNotExist:
            error_message = "Invalid card."
    select = request.GET.get("select")
    select_card = None
    if select:
        try:
            select_card = int(select)
        except ValueError:
            pass
    return render(
        request,
        "orders/checkout_card.html",
        {"error_message": error_message, "select_card": select_card},
    )


def get_order(request):
    order_sess = request.session.get("order")
    if order_sess is not None:
        for obj in serializers.deserialize("json", order_sess):
            order = obj.object
        return order


def keep_order(request, order):
    request.session["order"] = serializers.serialize("json", [order])


@login_required
def checkout_confirm(request):
    order = get_order(request)
    cart = request.session.get("cart")
    if (
        order is None
        or order.address_zip is None
        or request.session.get("checkout_cvc") is None
        or cart is None
        or len(cart) == 0
    ):
        raise PermissionDenied
    date_diff = now() - order.date
    if date_diff.days > 1:
        raise PermissionDenied
    if request.method == "POST":
        order.date = now()
        order.status = Status.objects.get(name="Placed")
        order.save()
        for obj in serializers.deserialize("json", request.session.get("order_items")):
            order_item = obj.object
            order_item.order_id = order.id
            order_item.save()
        request.session["last_order_completed"] = serializers.serialize("json", [order])
        del request.session["order"]
        del request.session["order_items"]
        del request.session["cart"]
        del request.session["cart_total"]
        return redirect("checkout_finished")
    order.first_name = request.user.first_name
    order.last_name = request.user.last_name
    order.phone_number = request.user.profile.phone
    order.user_id = request.user.id
    keep_order(request, order)
    for obj in serializers.deserialize("json", request.session.get("checkout_card")):
        card = obj.object
    order_items = []
    for obj in serializers.deserialize("json", request.session.get("order_items")):
        order_items.append(obj.object)
    return render(
        request,
        "orders/checkout_confirm.html",
        {"order": order, "order_items": order_items, "card": card},
    )


@login_required
def checkout_finished(request):
    last_order_completed = request.session.get("last_order_completed")
    if last_order_completed is not None:
        for obj in serializers.deserialize("json", last_order_completed):
            order = obj.object
        del request.session["last_order_completed"]
        return render(request, "orders/checkout_finished.html", {"order_id": order.id})
    raise PermissionDenied
