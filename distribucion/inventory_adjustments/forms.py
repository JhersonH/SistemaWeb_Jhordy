from django import forms
from .models import InventoryAdjustment

class InventoryAdjustmentForm(forms.ModelForm):
    class Meta:
        model = InventoryAdjustment
        fields = ['product', 'location', 'quantity', 'adjustment_type', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
