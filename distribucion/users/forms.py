# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile
from roles.models import Role

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=False)
    is_active = forms.BooleanField(required=False, initial=True, label="Activo")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_active")

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_active")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "role", "doc_id", "phone", "avatar",
            "birth_date", "address", "hire_date", "position"
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "hire_date": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 2}),
        }

class AdminSetPasswordForm(SetPasswordForm):
    """Para que un admin cambie la contraseña de otro usuario."""
    pass

class UserProfileUpdateForm(forms.ModelForm):
    new_password = forms.CharField(
        label="Nueva contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Dejar vacío para no cambiarla'}),
        help_text="Déjalo vacío si no deseas cambiar tu contraseña."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
