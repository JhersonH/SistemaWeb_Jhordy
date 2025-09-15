from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
import unicodedata

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrecta.")
        return super().form_invalid(form)

@login_required
def dashboard(request):
    return render(request, 'dashboard/home.html')

def normalize_string(value):
    return ''.join(
        c for c in unicodedata.normalize('NFD', value)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# Función auxiliar para convertir día a índice FullCalendar (0=domingo, ..., 6=sábado)
def get_day_index(day):
    days = {
        'domingo': 0,
        'lunes': 1,
        'martes': 2,
        'miércoles': 3,
        'miercoles': 3,
        'jueves': 4,
        'viernes': 5,
        'sábado': 6,
        'sabado': 6
    }
    return days.get(day.lower(), 0)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'dashboard/change_password.html'
    success_url = reverse_lazy('teacher_profile')

    def form_valid(self, form):
        messages.success(self.request, _('Tu contraseña ha sido actualizada correctamente.'))
        return super().form_valid(form)

def custom_permission_denied_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)
