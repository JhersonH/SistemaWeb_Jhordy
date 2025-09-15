from django import forms
from .models import UserPreference

class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['language', 'dark_mode', 'email_notifications']
        labels = {
            'language': 'Idioma',
            'dark_mode': 'Modo Oscuro',
            'email_notifications': 'Recibir notificaciones por correo'
        }
