from django.contrib import admin
from .models import StockAlert

@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ('product', 'location', 'minimum_quantity', 'created_at')
    list_filter = ('location',)
