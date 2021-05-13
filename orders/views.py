from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect
from django.utils.timezone import now

from orders.models import Status


@login_required
def checkout_address(request):
    """View where the user selects the address he want's to use for his current order."""
    error_message = None
    order = get_order(request)
    cart = request.session.get("cart")
    # If the user does not have an order or his cart is empty, then he gets denied.
    if order is None or cart is None or len(cart) == 0:
        raise PermissionDenied
    if request.method == "POST":
        try:
            # When the address has been selected and sent it adds it to the order
            # that he is currently working on.
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
    # Gets before selected address if there is one.
    select = request.GET.get("select")
    select_address = None
    if select:
        # Makes it an int so it's easier to work with in the template.
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
    """View where the user selects the card he want's to use for his current order."""

    error_message = None
    order = get_order(request)
    cart = request.session.get("cart")
    # If the user does not have an order, or has not selected an address for it or does
    # not have a cart then he gets denied access to the page.
    if order is None or order.address_zip is None or cart is None or len(cart) == 0:
        raise PermissionDenied
    if request.method == "POST":
        cvc = request.POST.get("CVCfield")
        # Checks if the cvc and card if they are valid and if so stores them.
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
    # Gets before selected card if there is one.
    select = request.GET.get("select")
    select_card = None
    if select:
        # Makes it an int so it's easier to work with in the template.
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
    """Retrieves the users current order from temporary storage."""
    order_sess = request.session.get("order")
    if order_sess is not None:
        for obj in serializers.deserialize("json", order_sess):
            order = obj.object
        return order


def keep_order(request, order):
    """Saves the users order into temporary storage."""
    request.session["order"] = serializers.serialize("json", [order])


def are_products_in_stock(request):
    """Checks if all products that the user wants to buy are truly in stock,
    returns the items and error/s if any are not in stock."""
    errors = []
    order_items = []
    for obj in serializers.deserialize("json", request.session.get("order_items")):
        order_item = obj.object
        order_items.append(order_item)
        product = order_item.product
        if (order_item.quantity > product.stock):
            errors.append(f"Not enough in stock to buy {product.name}.")
    return (errors, order_items)


@login_required
def checkout_confirm(request):
    """View for confirming the users order, if he confirms it saves
    the order to the database and does all appropriate actions as well."""
    order = get_order(request)
    cart = request.session.get("cart")
    # If the user has no order, no cart or has not chosen an
    # address or card for the order then it denies him access to the page.
    if (
        order is None
        or order.address_zip is None
        or request.session.get("checkout_cvc") is None
        or cart is None
        or len(cart) == 0
    ):
        raise PermissionDenied
    # Checks if the order is older than a day and if so it denies the user access as
    # we only want orders to be available for a day else it could cause issues.
    date_diff = now() - order.date
    if date_diff.days > 1:
        raise PermissionDenied
    # Gets the users card from temporary storage.
    for obj in serializers.deserialize("json", request.session.get("checkout_card")):
        card = obj.object
    if request.method == "POST":
        stock_errors, order_items = are_products_in_stock(request)
        if len(stock_errors) > 0:
            # If a product or multiple product are not in stock it will cancel
            # the order and return to the same screen with the errors up.
            return render(
                request,
                "orders/checkout_confirm.html",
                {"order": order, "order_items": order_items, "card": card, "stock_errors": stock_errors},
            )
        # Saves the order to the database with all it's order items.
        order.date = now()
        order.status = Status.objects.get(name="Placed")
        order.save()
        for order_item in order_items:
            order_item.order_id = order.id
            product = order_item.product
            product.stock -= order_item.quantity
            product.save()
            order_item.save()
        request.session["last_order_completed"] = serializers.serialize("json", [order])
        # Deletes everything from temporary storage that was used while
        # making the order as it has been saved to the database.
        del request.session["order"]
        del request.session["order_items"]
        del request.session["cart"]
        del request.session["cart_total"]
        del request.session["checkout_card"]
        del request.session["checkout_cvc"]
        return redirect("checkout_finished")
    order.first_name = request.user.first_name
    order.last_name = request.user.last_name
    order.phone_number = request.user.profile.phone
    order.user_id = request.user.id
    keep_order(request, order)
    # Gets all the order items for the current order which store the products the user is buying.
    order_items = []
    for obj in serializers.deserialize("json", request.session.get("order_items")):
        order_items.append(obj.object)
    return render(
        request,
        "orders/checkout_confirm.html",
        {"order": order, "order_items": order_items, "card": card, "stock_errors": None},
    )


@login_required
def checkout_finished(request):
    """View that is only shown when products have just been purchased."""
    last_order_completed = request.session.get("last_order_completed")
    if last_order_completed is not None:
        # If there is a recent order it continues to the view.
        # Gets the order to be able to display the order id on the finished page.
        for obj in serializers.deserialize("json", last_order_completed):
            order = obj.object
        # Deletes it from temporary storage so this screen can't be loaded again
        # unless a new order comes through.
        del request.session["last_order_completed"]
        return render(request, "orders/checkout_finished.html", {"order_id": order.id})
    raise PermissionDenied
