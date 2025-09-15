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
    role = forms.ModelChoiceField(
        queryset=Role.objects.filter(is_active=True).order_by("role_type"),
        required=False,
        empty_label="-- Selecciona un rol --",
        label="Rol"
    )

    class Meta:
        model = Profile
        fields = ("role", "doc_id", "phone", "avatar")

class AdminSetPasswordForm(SetPasswordForm):
    """Para que un admin cambie la contraseña de otro usuario."""
    pass
