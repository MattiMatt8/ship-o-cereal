from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render


@login_required
def checkout_address(request): # TODO: Make sure cart is not empty
    checkout_address_id = request.session.get("checkout_address_id")
    return render(request, "orders/checkout_address.html", {
        "checkout_address_id": checkout_address_id
    }) # TODO: If user has no address, not continue, etc.


@login_required
def checkout_card(request): # TODO: Make sure address has been selected & cart not empty
    checkout_card_id = request.session.get("checkout_card_id")
    return render(request, "orders/checkout_card.html", {
        "checkout_card_id": checkout_card_id
    }) # If user has no address, not continue, etc.


def choose_address(request, id):
    if request.method == "POST":
        try:
            address = request.user.address_set.get(pk=id) # Make sure user has the address
            for obj in serializers.deserialize("json", request.session.get("order")):
                order = obj.object
            order.address_id = address.id
            request.session["order"] = serializers.serialize("json", [order])
            return JsonResponse({"message":"Success"}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Error: Address not found."}, status=404)
    return JsonResponse({"message": "Error: Method not supported."}, status=405)


def choose_card(request, id):
    if request.method == "POST":
        try:
            card = request.user.card_set.get(pk=id) # Make sure user has the card
            for obj in serializers.deserialize("json", request.session.get("order")):
                order = obj.object
            order.card_id = card.id
            request.session["order"] = serializers.serialize("json", [order])
            return JsonResponse({"message":"Success"}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Error: Card not found."}, status=404)
    return JsonResponse({"message": "Error: Method not supported."}, status=405)


@login_required
def checkout_confirm(request): # TODO: Make sure address and card have been selected & cart not empty
    return render(request, "orders/checkout_confirm.html")


def checkout_finished(request):
    return render(request, "orders/checkout_finished.html")
