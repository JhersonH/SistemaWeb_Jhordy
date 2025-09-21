from django.contrib import admin
from .models import InventoryAdjustment

@admin.register(InventoryAdjustment)
class InventoryAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('product', 'location', 'adjustment_type', 'quantity', 'reason', 'created_at')
    list_filter = ('adjustment_type', 'location')
