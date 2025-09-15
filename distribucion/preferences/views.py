from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import UserPreference
from .forms import UserPreferencesForm
from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.translation import gettext as _

@login_required
def configuration_view(request):
    preferences, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            preferences = form.save()
            language = preferences.language

            # 🔁 Activa idioma en el momento
            translation.activate(language)

            # ✅ Guarda en sesión y en cookie
            request.session['django_language'] = language
            response = HttpResponseRedirect(reverse('configuration'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)

            messages.success(request, _("Preferencias guardadas correctamente."))
            return response
    else:
        form = UserPreferencesForm(instance=preferences)

    return render(request, 'dashboard/settings.html', {
        'form': form,
        'preferences': preferences
    })

@login_required
def set_user_language(request):
    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=request.user.preferences)
        if form.is_valid():
            preferences = form.save(commit=False)
            preferences.user = request.user
            preferences.save()

            # 🔄 Establecer el idioma en la sesión inmediatamente
            request.session[settings.LANGUAGE_COOKIE_NAME] = preferences.language

            messages.success(request, "Preferencias actualizadas correctamente.")
            return redirect('user_preferences')
        else:
            messages.error(request, "Error al guardar preferencias.")
    else:
        form = UserPreferencesForm(instance=request.user.preferences)

    return render(request, 'preferences/user_preferences.html', {'form': form})

@csrf_exempt
@login_required
def toggle_dark_mode(request):
    if request.method == 'POST':
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        preferences.dark_mode = not preferences.dark_mode
        preferences.save()
        return JsonResponse({'dark_mode': preferences.dark_mode})
    return JsonResponse({'error': 'Invalid request'}, status=400)