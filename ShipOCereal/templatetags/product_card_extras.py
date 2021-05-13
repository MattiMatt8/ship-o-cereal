from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    """Used to get how much of an item user has in its
    cart from a template anywhere in the app."""
    if dictionary is None:
        return None
    return dictionary.get(str(key))
