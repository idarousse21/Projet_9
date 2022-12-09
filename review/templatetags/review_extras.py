from django.template import Library

register = Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def get_range(number):
    return range(int(number))


