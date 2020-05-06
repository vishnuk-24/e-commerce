from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from products.models import Product

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
