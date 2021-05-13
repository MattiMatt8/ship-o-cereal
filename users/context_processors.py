def cart_count(request):
    """Context proccessor to give us access the how many items are
    in the cart on all pages."""
    cart_total = request.session.get("cart_total")
    return {"total_in_cart": cart_total if cart_total else 0}