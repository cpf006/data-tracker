from django import template

register = template.Library()

@register.filter()
def leftovers(val, divisable):
    return range(divisable - (val % divisable))