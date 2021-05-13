from products.models import Category, Brand, Label


def menu_categories(request):
    """Context processor that provides access to product categories as a context variable."""

    return {"categories": Category.objects.all()}


def product_brands(request):
    """Context processor that provides access to product brands as a context variable."""

    return {"brands": Brand.objects.all()}


def product_labels(request):
    """Context processor that provides access to product labels as a context variable."""

    return {"labels": Label.objects.all()}


def get_cart(request):
    """Context processor to be able to access the cart on every page."""
    return {"cart": request.session.get("cart")}
