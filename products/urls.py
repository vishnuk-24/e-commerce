
from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    # path('products/', views.ProductListView.as_view(), name="products"),
    # path('product-detail/(?P<pk>[0-9a-f-]+)/$', views.ProductDetailView.as_view(), name="product_detail"),
]

# url(r'^products/$', views.ProductListView.as_view(), name="products"),
# url(r'^product-detail/(?P<pk>[0-9]+)/$', views.ProductDetailView.as_view(), name="product_detail"),
