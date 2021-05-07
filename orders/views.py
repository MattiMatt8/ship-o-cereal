from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from users.models import Address


@login_required
def checkout_address(request): # TODO: Make sure cart is not empty
    return render(request, "orders/checkout_address.html") # TODO: If user has no address, not continue, etc.


def choose_address(request, id):
    request.session["checkout_address_id"] = id
    print(request.session["checkout_address_id"])
    return JsonResponse({"message":"success"})


@login_required
def checkout_card(request): # TODO: Make sure address has been selected & cart not empty
    return render(request, "orders/checkout_card.html") # If user has no address, not continue, etc.


def choose_card(request, id):
    pass


@login_required
def checkout_confirm(request): # TODO: Make sure address and card have been selected & cart not empty
    return render(request, "orders/checkout_confirm.html")


def checkout_finished(request):
    return render(request, "orders/checkout_finished.html")
