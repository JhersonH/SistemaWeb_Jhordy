# product_categories/forms.py

from django import forms
from .models import ProductCategory

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
