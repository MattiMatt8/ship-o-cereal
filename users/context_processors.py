
def cart_count(request):
    cart = request.session.get("cart")
    total = 0
    if cart:
        for value in cart.values():
            total += value
    return {"total_in_cart": total}