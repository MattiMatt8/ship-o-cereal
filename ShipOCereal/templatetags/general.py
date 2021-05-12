from django.template.defaulttags import register


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter(name='times')
def times(number):
    return range(int(number))

@register.filter(name='get_unfilled_stars')
def get_unfilled_stars(number):
    return range(5 - int(number))
