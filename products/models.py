""" Products/models """

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

from core.models import BaseModel

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Brand(BaseModel):
    """Brand model for store each brands"""

    name = models.CharField(max_length=64, blank=True, null=True)
    logo = models.ImageField(upload_to='products/brand-logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "not available"

    def get_image_url(self):
        if self.logo:
            return self.logo.url
        return "{}defaults/brand-logo.jpg".format(settings.MEDIA_URL)


class Category(BaseModel):
    """Category model for add each products category."""

    name = models.CharField(max_length=124, blank=True, null=True)
    logo = models.ImageField(upload_to='products/category-logos', blank=True, null=True)
    banner_image = models.ImageField(upload_to='products/banner-image', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    base_category = models.ForeignKey('self', blank=True, null=True, db_index=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name if self.name else "not available"

    def is_base(self):
        return True if self.base_category is None else False

    def get_image_url(self):
        if self.logo:
            return self.logo.url
        return "{}defaults/category-logo.jpg".format(settings.MEDIA_URL)

    def get_banner_image_url(self):
        if self.banner_image:
            return self.banner_image.url
        return "{}defaults/banner-image.png".format(settings.MEDIA_URL)


class Product(BaseModel):
    """Product model for store each items"""

    name = models.CharField(max_length=256, blank=True, null=True)
    product_model = models.CharField(max_length=200, blank=True, null=True)
    brand = models.ForeignKey(Brand, verbose_name=("brand name"), on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name=("Category name"), on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/product-images', blank=True, null=True)

    price = models.DecimalField(blank=True, null=True, max_digits=16, decimal_places=2)
    discount_price = models.DecimalField(blank=True, null=True, max_digits=16, decimal_places=2)
    price_unit = models.CharField(max_length=32, blank=True, null=True)

    count = models.IntegerField(default=0)
    maximum_purchase_limit_for_a_customer = models.PositiveIntegerField(default=5)
    enabled = models.BooleanField(default=True)


    def __str__(self):
        return self.name if self.name else "not available"

    def get_image_url(self):
        if self.image:
            return self.image.url
        return "{}defaults/product-image.jpg".format(settings.MEDIA_URL)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'pk': self.pk})

class Cart(BaseModel):
    """Cart model for the adding order items to cart."""

    user = models.ForeignKey(User, verbose_name=("register user"), on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, verbose_name=("order item"), on_delete=models.CASCADE, db_index=True)
    discounted_rate = models.DecimalField(blank=True, null=True, max_digits=16, decimal_places=2)
    discount_on_product = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    no_of_pieces = models.IntegerField(default=0)
    is_purchased = models.BooleanField(default=False)
    purchased_price = models.DecimalField(blank=True, null=True, max_digits=16, decimal_places=2)
    purchased_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.product.name

    def get_amount(self):
        rate = 0
        try:
            if self.offer.offer_type == "combo":

                oncombo, offcombo = divmod(self.no_of_pieces, self.offer.combo_no)
                combo_rate, non_rate = oncombo*self.offer.combo_amount, offcombo*self.product.price
                rate = combo_rate + non_rate

            elif self.offer.offer_type == "free":
                # counts of products alteration
                rate = self.product.price * self.no_of_pieces

            elif self.offer.offer_type == "discount":
                # counts of products alteration
                rate = (self.product.price - ((self.product.price*self.offer.discount_percentage)/100)) * self.no_of_pieces
        except AttributeError:
                rate = self.product.price * self.no_of_pieces
                
    def get_purchased_price(self):
        return self.purchased_price*self.no_of_pieces

