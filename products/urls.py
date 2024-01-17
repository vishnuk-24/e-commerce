"""Products urls.py"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'products'

urlpatterns = [

    path('', views.index, name='index'),

    path('home/', views.IndexListView.as_view(), name="home"),

    path('products/', views.ProductListView.as_view(), name="products"),

    path('product-detail/<pk>/', views.ProductDetailView.as_view(), name="product_detail"),

    path('add-to-cart/', views.AddToCartView.as_view(), name="add-to-cart"),

    path('categories/<pk>/', views.CategoryListView.as_view(), name="category_list"),
]
