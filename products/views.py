"""Products view.py"""

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.views.generic import View, ListView, DetailView
from django.views import View

from products.models import Brand, Cart, Category, Product

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class CategoryListView(View):
    """CategoryListView for listing all categories."""

    def get(self, request, *args, **kwargs):
        print('ENTER INTO CategoryListView')
        category_id = self.kwargs['pk']
        print('category_id', category_id)
        category = Category.objects.filter(base_category=category_id)
        print('category', category)
        if not category:
            return redirect(reverse('products:products'))
        search_value = self.request.GET.get('search', '')
        if search_value:
            category = Category.objects.filter(base_category=category_id, name__icontains=search_value)
            return render(request, 'products/categorylist.html', context={'categories': category})
        return render(request, 'products/categorylist.html', context={'categories': category})


class IndexListView(ListView):
    """IndexView for the listing a 6 new products into home page."""

    context_object_name = 'product_list'
    model = Product
    template_name = 'products/base.html'

    def get_queryset(self):
        print('ENTER INTO QUERYSET')
        queryset = Product.objects.all().select_related('brand', 'category').order_by("-created_on")[:6]
        print('queryset of select_related', queryset)
        return queryset


class ProductListView(ListView):
    """ProductListView for the list all the prodcts."""

    context_object_name = 'product_list'
    template_name = 'products/product-list.html'
    paginate_by = 2
    url_keys = list()


    def get_queryset(self):
        print('ENTER INTO QUERYSET')
        queryset = Product.objects.all().select_related('brand', 'category')
        print('queryset of select_related', queryset)
        print('GET keys', self.request.GET.keys())
        if 'brand_id' in self.request.GET.keys():
            queryset = queryset.filter(brand=self.request.GET['brand_id'])
            self.url_keys.append("brand_id={}".format(self.request.GET["brand_id"]))
        if "category_id" in self.request.GET.keys():
            queryset1 = queryset.filter(category=self.request.GET["category_id"])
            print('actual queryset1', queryset1)
            if not queryset1:
                cat = Category.objects.get(id=self.request.GET["category_id"])
                if cat.is_base():
                    queryset1 = queryset.filter(category__base_category=self.request.GET["category_id"])
                    print('queryset1 inside the is_base()', queryset1)
            queryset = queryset1
            self.url_keys.append("category_id={}".format(self.request.GET["category_id"]))
        return queryset

    def get_context_data(self, **kwargs):
        print('ENTER INTO GET_CONTEXT_DATA')
        context = super(ProductListView, self).get_context_data(**kwargs)
        print('context', context)
        context['category'] = Category.objects.all().exclude(name="not available")
        context['brands'] = Brand.objects.all().exclude(name="not available")
        print('context with band and category', context)
        return context



class ProductDetailView(DetailView):
    """ProductDetailView for the details of a product."""

    model = Product
    template_name = 'products/product-page.html'
    context_object_name = 'product'

    def get_queryset(self):
        print('ENTER INTO QUERYSET')
        product = self.model.objects.exclude(enabled=False)
        print('queryset', product)
        return product

    def get_context_data(self, **kwargs):
        print('ENTER INTO GET_CONTEXT_DATA')
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        print('self.kwargs[]', self.kwargs['pk'])
        context['brand'] = Product.objects.get(pk=self.kwargs['pk']).brand.name
        print('context', context)
        return context


class AddToCartView(View):
    """AddtoCartView for adding all order items."""

    def post(self, request):
        product_id = self.request.POST.get('product_id', None)
        quantity = self.request.POST.get('quantity', None)
        print('product_id', product_id)
        print('quantity', quantity)

        product = Product.objects.get(pk=product_id)
        print('product', product)

        if int(quantity) < product.count+1:
            if request.user.is_authenticated():
                if product.price:
                    obj, flag = Cart.objects.get_or_create(
                        user = request.user,
                        product = product,
                        is_purchased = False
                    )
                    if obj.no_of_pieces > product.maximum_purchase_limit_for_a_customer-1:
                        status = 'Failed'
                        status_message = "Maximum limit reached."
                        data = {
                            'status': status,
                            'count': len(request.session['cart_product']) if 'cart_product' in request.session else 0,
                            'status_message': status_message
                        }
                        return JsonResponse(data)
                    if obj.no_of_pieces > product.count-1:
                        status = 'Failed'
                        status_message = "Out of stock."
                        data = {
                            'status': status,
                            'count': len(request.session['cart_product']) if 'cart_product' in request.session else 0,
                            'status_message': status_message
                        }
                        return JsonResponse(data)
                    if obj.no_of_pieces == product.count:
                        status = "Failed"
                        status_message = "All products already in the cart."
                    obj.no_of_pieces = int(quantity) if flag else (obj.no_of_pieces + int(quantity))
                    # offer not added

                    obj.save()
                    status = 'success'
                    status_message = "Added Successfully."
                else:
                    status = 'Failed'
                    status_message = "Product price not available."
                products_in_cart = Cart.objects.filter(user=request.user, is_purchased=False)
                cart_list = []
                for product in products_in_cart:
                    cart_list.append({'cartid': product.id,
                                      'id': product.product.id,
                                      'name': product.product.name,
                                      'image': str(product.product.
                                                   get_image_url()),
                                      'quantity': product.no_of_pieces})
                products_in_cart = products_in_cart.aggregate(
                                     Sum('no_of_pieces')
                                   )['no_of_pieces__sum']
                if not products_in_cart:
                    products_in_cart = 0
                data = {
                    'status': status,
                    'status_message': status_message,
                    'count': products_in_cart,
                    'cart_list': cart_list
                }
                return JsonResponse(data)
            else:
                if product.price:
                    if 'cart_product' in request.session:
                        print(request.session['cart_product'])
                        flag = True
                        for cindex in request.session['cart_product']:
                            if int(product_id) == int(cindex['id']):
                                if cindex['quantity'] > product.count - 1:
                                    status = 'Failed'
                                    status_message = "Out of stock."
                                    data = {
                                        'status': status,
                                        'status_message': status_message
                                    }
                                    return JsonResponse(data)
                                if (cindex['quantity']+int(quantity)) > product.count - 1:
                                    status = 'Failed'
                                    status_message = "Sorry not possible."
                                    data = {
                                        'status': status,
                                        'status_message': status_message
                                    }
                                    return JsonResponse(data)
                                print(cindex['quantity'], "before")
                                cindex['quantity'] += int(quantity)
                                flag = False
                                break
                        if flag:
                            request.session['cart_product'] += [{
                                'id': int(product_id),
                                'quantity': int(quantity)
                            }]
                    else:
                        request.session['cart_product'] = [{
                            'id': int(product_id),
                            'quantity': int(quantity)
                        }]
                    request.session.save()
                    cart_list = []
                    count_list = 0
                    for product in request.session['cart_product']:
                        item = Product.objects.get(id=product['id'])
                        count_list += product['quantity']
                        cart_list.append({'id': product['id'],
                                          'name': item.name,
                                          'image': str(item.get_image_url()),
                                          'quantity': int(product['quantity'])})

                    status = 'success'
                    status_message = "Added Successfully."
                    data = {
                        'status': status,
                        'count': count_list,
                        'cart_list': cart_list,
                        'status_message': status_message
                    }
                    print(request.session['cart_product'][0]['quantity'])
                else:
                    status = 'Failed'
                    status_message = "Product price not available."
                    data = {
                        'status': status,
                        'count': len(request.session['cart_product']) if 'cart_product' in request.session else 0,
                        'status_message': status_message

                    }
                return JsonResponse(data)
        else:
            status = 'Failed'
            status_message = 'Product quality is not available'
            data = {
                'status': status,
                'count': len(request.session['cart_product']) if 'cart_product' in request.session else 0,
                'status_message': status_message
            }
            return JsonResponse(data)
