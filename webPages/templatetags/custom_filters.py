from django import template

register = template.Library()

@register.filter
def custom_slice(value, arg):
    try:
        return value[int(arg):]
    except (ValueError, IndexError):
        return value