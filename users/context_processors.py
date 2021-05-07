
def cart_count(request):
    cart_total = request.session.get("cart_total")
    return {"total_in_cart": cart_total if cart_total else 0}