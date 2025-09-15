from django.urls import path

from preferences.views import configuration_view, toggle_dark_mode
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('configuration/', configuration_view, name='configuration'),
    path('toggle-dark-mode/', toggle_dark_mode, name='toggle_dark_mode'),
]
