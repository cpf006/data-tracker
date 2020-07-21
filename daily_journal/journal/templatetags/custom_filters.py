from django import template

register = template.Library()

@register.filter()
def leftovers(val, divisable):
    return range(divisable - (val % divisable))

@register.filter
def get(dict, key):    
    return dict.get(key)

