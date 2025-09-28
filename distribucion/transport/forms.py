from django import forms
from .models import Vehicle, Driver, Route, Trip, Stop, Expense, Incident
from django.forms import inlineformset_factory
from .models import TripProduct

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        labels = {
            'plate': 'Placa del vehículo',
            'brand': 'Marca',
            'model': 'Modelo',
            'year': 'Año',
            'capacity_kg': 'Capacidad (kg)',
            'volume_m3': 'Volumen (m³)',
            'status': 'Estado',
            'odometer_km': 'Kilometraje',
            'insurance_expiry': 'Fecha de vencimiento del SOAT/Seguro',
            'next_maintenance': 'Próximo mantenimiento',
        }
        widgets = {
            'insurance_expiry': forms.DateInput(
                attrs={
                    'class': 'form-control datepicker',
                    'placeholder': 'dd-mm-aaaa'
                },
                format='%d-%m-%Y'
            ),
            'next_maintenance': forms.DateInput(
                attrs={
                    'class': 'form-control datepicker',
                    'placeholder': 'dd-mm-aaaa'
                },
                format='%d-%m-%Y'
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['insurance_expiry'].input_formats = ['%d-%m-%Y']
        self.fields['next_maintenance'].input_formats = ['%d-%m-%Y']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
        labels = {
            'license_expiry': 'Vencimiento de Licencia',
            'license_category': 'Categoría de Licencia'
        }
        widgets = {
            'license_expiry': forms.DateInput(
                attrs={
                    'class': 'form-control datepicker',
                    'placeholder': 'dd-mm-aaaa'
                },
                format='%d-%m-%Y'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['license_expiry'].input_formats = ['%d-%m-%Y']

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
        labels = {
            'code': 'Código del viaje',
            'date': 'Fecha del viaje',
            'route': 'Ruta asignada',
            'vehicle': 'Vehículo',
            'driver': 'Conductor',
            'status': 'Estado',
            'odometer_start': 'Odómetro de salida (km)',
            'odometer_end': 'Odómetro de llegada (km)',
            'notes': 'Notas u observaciones',
        }
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'class': 'form-control datepicker',
                    'placeholder': 'dd-mm-aaaa'
                },
                format='%d-%m-%Y'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%d-%m-%Y']

        if self.instance and self.instance.pk:
            self.fields.pop('is_reception', None)

class TripProductForm(forms.ModelForm):
    class Meta:
        model = TripProduct
        fields = ["product", "quantity"]

TripProductFormSet = inlineformset_factory(
    Trip,
    TripProduct,
    form=TripProductForm,
    extra=1,
    can_delete=True
)

class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        exclude = ['trip']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = '__all__'
        widgets = {
            'occurred_at': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            occurred_at = self.instance.occurred_at
            if occurred_at:
                self.fields['occurred_at'].initial = occurred_at.strftime('%Y-%m-%dT%H:%M')