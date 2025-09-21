# inventory_kardex/forms.py
from django import forms
from inventory_product.models import Product

class KardexFilterForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False,
        label="Producto",
        empty_label="Seleccione un producto",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
