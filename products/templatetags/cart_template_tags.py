from django import template
from products.models import Cart

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user, is_purchased=False)
        # if qs.exists():
        #     return qs[0].product.count()
    return 0
