"""e_commerce/context_processors.py"""

from django.db.models import Q
from django.views.generic import View
from products.models import Category, Brand


def site_config_processor(request):
    """site_config_processor for provide category and brand for the each product list."""
    header_category = Category.objects.all().exclude(Q(name='')).order_by('name')
    header_brand = Brand.objects.all().order_by('name')
    IndexCategory = header_category.filter(base_category=None).order_by('name')
    context = {
        'header_category': header_category,
        'header_brand': header_brand,
        'IndexCategory': IndexCategory
    }
    return context