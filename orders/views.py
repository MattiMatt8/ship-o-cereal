from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from users.models import Address


@login_required
def checkout_address(request): # TODO: Make sure cart is not empty
    checkout_address_id = request.session.get("checkout_address_id")
    return render(request, "orders/checkout_address.html", {
        "checkout_address_id": checkout_address_id
    }) # TODO: If user has no address, not continue, etc.


def choose_address(request, id):
    request.session["checkout_address_id"] = id
    return JsonResponse({"message":"success"})


@login_required
def checkout_card(request): # TODO: Make sure address has been selected & cart not empty
    checkout_card_id = request.session.get("checkout_card_id")
    return render(request, "orders/checkout_card.html", {
        "checkout_card_id": checkout_card_id
    }) # If user has no address, not continue, etc.


def choose_card(request, id):
    request.session["checkout_card_id"] = id
    return JsonResponse({"message":"success"})


@login_required
def checkout_confirm(request): # TODO: Make sure address and card have been selected & cart not empty
    return render(request, "orders/checkout_confirm.html")


def checkout_finished(request):
    return render(request, "orders/checkout_finished.html")
