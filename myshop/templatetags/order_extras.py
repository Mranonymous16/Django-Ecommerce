# from django import template

# register = template.Library()

# @register.filter
# def multiply(value, arg):
#     return value * arg

# myshop/templatetags/order_extras.py

# myshop/templatetags/order_extras.py
from django import template

register = template.Library()

@register.filter
def multiply(price, quantity):
    """Multiplies price by quantity."""
    try:
        return float(price) * float(quantity)
    except (ValueError, TypeError):
        return ''

@register.filter(name='get_total')
def get_total(order):
    """Calculates total cost of all items in the order."""
    try:
        return sum(item.product.price * item.quantity for item in order.items.all())
    except:
        return ''
