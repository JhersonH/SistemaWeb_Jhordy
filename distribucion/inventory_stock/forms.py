# inventory_stock/forms.py

from django import forms
from .models import ProductStock
from .models import StockLocation

class ProductStockForm(forms.ModelForm):
    class Meta:
        model = ProductStock
        fields = ['product', 'location', 'quantity']

class StockLocationForm(forms.ModelForm):
    class Meta:
        model = StockLocation
        fields = ['name', 'description']
