from django.contrib import admin
from .models import StockLocation, ProductStock

@admin.register(StockLocation)
class StockLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'location', 'quantity')
    list_filter = ('location',)
