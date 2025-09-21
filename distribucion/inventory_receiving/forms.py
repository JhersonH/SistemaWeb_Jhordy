from django import forms
from .models import ProductReception
from transport.models import Trip

class ProductReceptionForm(forms.ModelForm):
    class Meta:
        model = ProductReception
        fields = ['product', 'quantity_received', 'supplier', 'location', 'notes', 'receiver', 'trip']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mostrar solo viajes válidos
        self.fields['trip'].queryset = Trip.objects.filter(
            is_reception=True
        ).exclude(status__in=['completed', 'canceled'])

        # Hacemos que sea opcional desde el punto de vista del formulario
        self.fields['quantity_received'].required = False

        # Si ya hay viaje, lo desactivamos visualmente
        if self.instance and self.instance.trip:
            self.fields['quantity_received'].widget.attrs['readonly'] = True
            self.fields['quantity_received'].widget.attrs['style'] = 'background-color:#eee; cursor:not-allowed;'
