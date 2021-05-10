from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.timezone import now


@login_required
def checkout_address(request):  # TODO: Make sure cart is not empty
    # TODO: Go back to address page address is selected but can't continue
    # TODO: address not on the user error
    error_message = None
    order = get_order(request)
    if order is None:
        print("Error does not have an order") # TODO: What shall I do here?
    if (request.method == "POST"):
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
    return render(
        request, "orders/checkout_address.html",
        {"error_message": error_message}
    )


@login_required
def checkout_card(request):
    # TODO: Make sure address has been selected & cart not empty
    # TODO: Go back to address page address is selected but can't continue
    error_message = None
    order = get_order(request)  # TODO: Check stuff with and stuff
    if order is None:
        print("Error does not have an order") # TODO: What shall I do here?
    elif order.address_zip is None:
        print("Error address has not been selected") # TODO: What shall I do here?
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
    return render(
        request,
        "orders/checkout_card.html",
        {"error_message": error_message},
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
    # TODO: Make sure address and card have been selected & cart not empty
    order = get_order(request)
    if order is None:
        print("Error does not have an order") # TODO: What shall I do here?
    elif order.address_zip is None:
        print("Error address has not been selected") # TODO: What shall I do here?
    elif request.session.get("checkout_cvc") is None:
        print("Error card has not been selected") # TODO: What shall I do here
    date_diff = now() - order.date
    if date_diff.days > 1:
        print("Order invalid") # TODO: What shall I do here
    if request.method == "POST":
        order.date = now()
        order.status = "Placed"
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
        {  # TODO: Probably pass in card, address and user as well
            "order": order,
            "order_items": order_items,
            "card": card
        },
    )


@login_required
def checkout_finished(request):
    # TODO: Some checks that the user just did finish an order and so forth
    last_order_completed = request.session.get("last_order_completed")
    if last_order_completed is not None:
        for obj in serializers.deserialize("json", last_order_completed):
            order = obj.object
        del request.session["last_order_completed"]
        return render(request, "orders/checkout_finished.html", {"order_id": order.id})
    return render(request, "orders/checkout_finished.html") # TODO: Different view or redirect?
