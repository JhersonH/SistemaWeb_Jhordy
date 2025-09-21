# inventory_product/forms.py
from django import forms
from .models import Product
from product_categories.models import ProductCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'unit', 'min_stock', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
