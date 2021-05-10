from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now


@login_required
def checkout_address(request):  # TODO: Make sure cart is not empty
    if (
        request.method == "POST"
    ):  # TODO: Go back to address page address is selected but can't continue
        order = get_order(request)
        cvc = request.POST.get("CVCfield")
        print("Das post:", request.POST)
    return render(
        request, "orders/checkout_address.html"
    )  # TODO: If user has no address, not continue, etc.


@login_required
def checkout_card(
    request,
):  # TODO: Make sure address has been selected & cart not empty
    cvc_error = (
        None  # TODO: Go back to address page address is selected but can't continue
    )
    if request.method == "POST":
        cvc = request.POST.get("CVCfield")
        print("Das post:", request.POST)
        try:
            cvc_int = int(cvc)
            if len(cvc) != 3:
                raise ValueError
            request.session["card_cvc"] = cvc_int
            return redirect("checkout_confirm")
        except ValueError:
            cvc_error = "Invalid CVC number."
    order = get_order(request)
    return render(
        request,
        "orders/checkout_card.html",
        {"checkout_card_id": order.card_id, "cvc_error": cvc_error},
    )  # If user has no address, not continue, etc.


def get_order(request):
    order_sess = request.session.get("order")
    if order_sess is not None:
        for obj in serializers.deserialize("json", order_sess):
            order = obj.object
        return order


def set_address_in_order(request, id):
    order = get_order(request)
    order.address_id = id
    request.session["order"] = serializers.serialize("json", [order])


def choose_address(request, id):  # TODO: AXIOS Call move to view ting form ting
    if request.method == "POST":
        try:
            address = request.user.address_set.get(
                pk=id
            )  # Make sure user has the address
            set_address_in_order(request, address.id)
            return JsonResponse({"message": "Success"}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Error: Address not found."}, status=404)
    return JsonResponse({"message": "Error: Method not supported."}, status=405)


def set_card_in_order(request, id):
    order = get_order(request)
    order.card_id = id
    request.session["order"] = serializers.serialize("json", [order])


def choose_card(request, id):  # AXIOS call move to card view ting select ting
    if request.method == "POST":
        try:
            card = request.user.card_set.get(pk=id)  # Make sure user has the card
            set_card_in_order(request, card.id)
            return JsonResponse({"message": "Success"}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Error: Card not found."}, status=404)
    return JsonResponse({"message": "Error: Method not supported."}, status=405)


@login_required
def checkout_confirm(
    request,
):  # TODO: Make sure address and card have been selected & cart not empty
    if request.method == "POST":  # TODO: CHECK IF DATE IS TO OLD MAYBE REJECT?
        order = get_order(request)
        order.user_id = request.user.id
        order.date = now()
        order.status = "Placed"
        order.save()
        for obj in serializers.deserialize("json", request.session.get("order_items")):
            order_item = obj.object
            order_item.order_id = order.id
            order_item.save()
        del request.session["order"]
        del request.session["order_items"]
        del request.session["cart"]
        return redirect("checkout_finished")
        # TODO: CLEAR CASH
    order = get_order(request)
    order_items = []
    for obj in serializers.deserialize("json", request.session.get("order_items")):
        order_items.append(obj.object)
    return render(
        request,
        "orders/checkout_confirm.html",
        {  # TODO: Probably pass in card, address and user as well
            "order": order,
            "order_items": order_items,
        },
    )


def checkout_finished(request):
    return render(request, "orders/checkout_finished.html")
