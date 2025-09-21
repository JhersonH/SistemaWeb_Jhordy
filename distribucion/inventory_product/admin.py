from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'unit', 'min_stock', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('category', 'is_active')
