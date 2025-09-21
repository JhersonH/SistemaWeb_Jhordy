from django.contrib import admin
from .models import KardexEntry

@admin.register(KardexEntry)
class KardexEntryAdmin(admin.ModelAdmin):
    list_display = ('product', 'location', 'entry_type', 'quantity', 'balance', 'date', 'reference')
    list_filter = ('entry_type', 'location')
    search_fields = ('product__name', 'reference')
