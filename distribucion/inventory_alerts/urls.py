from django.urls import path
from . import views

app_name = 'inventory_alerts'

urlpatterns = [
    path('', views.alert_list, name='alert_list'),
]
