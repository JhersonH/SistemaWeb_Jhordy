from django import forms
from .models import InventoryMovement
from inventory_stock.models import ProductStock

class InventoryMovementForm(forms.ModelForm):
    class Meta:
        model = InventoryMovement
        fields = ['product', 'quantity', 'movement_type', 'location', 'description', 'trip']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        location = cleaned_data.get("location")
        qty = cleaned_data.get("quantity")
        movement_type = cleaned_data.get("movement_type")
        trip = cleaned_data.get("trip")

        # Validación de stock
        if movement_type == "output" and product and location:
            stock = ProductStock.objects.filter(product=product, location=location).first()
            if not stock or stock.quantity < qty:
                raise forms.ValidationError(
                    f"No hay suficiente stock en {location}. Stock disponible: {stock.quantity if stock else 0}."
                )

        # Validación de viaje asociado
        if movement_type == "output" and not trip:
            raise forms.ValidationError("Debes asociar un viaje cuando el movimiento es una salida.")

        if movement_type != "output":
            cleaned_data["trip"] = None

        return cleaned_data
