from django.contrib import admin
from .models import InventoryMovement

@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'location', 'date', 'registered_by')
    list_filter = ('movement_type', 'location')
    search_fields = ('product__name',)
