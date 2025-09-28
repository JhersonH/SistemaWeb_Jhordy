from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre del proveedor"
            }),
            "contact_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Persona de contacto"
            }),
            "phone": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Teléfono",
                "min": "1000000",
                "max": "999999999999999"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "correo@dominio.com"
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Dirección completa"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
