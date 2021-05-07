from django.http import JsonResponse

from products.models import Product


class Cart(object):
    def __int__(self, session):
        self.cart = {}

    def add(self, id, quantity=1):
        product = Product.objects.all().get(pk=id)
        if product:
            if product in self.cart:
                self.cart[product] += quantity
            else:
                self.cart[product] = quantity
            return JsonResponse({"message": "Item added to cart."})
        return JsonResponse({"message": "Product was not found."})