from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from products.models import Product

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# class ProductListView(ListView):
#     """ProductListView for the list all the prodcts."""

#     context_object_name = 'product_list'
#     model = Product
#     template_name = 'product-page.html'

#     def def get_queryset(self):
#         queryset = super(CLASS_NAME, self).get_queryset()
#         queryset = queryset # TODO
#         return queryset