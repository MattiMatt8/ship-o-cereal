from products.models import Category


def menu_categories(request):
    """
    Context processor that provides access to product categories as context variables.
    """
    categories = Category.objects.all()

    return {"categories": categories}
