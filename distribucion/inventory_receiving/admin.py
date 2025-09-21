from django.contrib import admin
from .models import ProductReception

@admin.register(ProductReception)
class ProductReceptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_received', 'reception_date', 'supplier', 'location')
    search_fields = ('product__name', 'supplier')
    list_filter = ('location',)
