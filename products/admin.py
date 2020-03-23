""" Products/admin """

from django.contrib import admin

from products import models

@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "id")
    search_fields = ("name", "description", "id")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "id")
    search_fields = ("name", "description", "id")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product_model", "category", "brand", "price", "discount_price", "count")
    search_fields = ("id", "name", "description")
    list_filter = ("enabled",)
