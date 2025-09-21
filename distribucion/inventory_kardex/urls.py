# inventory_kardex/urls.py
from django.urls import path
from . import views

app_name = "inventory_kardex"

urlpatterns = [
    path('', views.kardex_list, name='kardex_list'),
    path('api/<int:product_id>/', views.kardex_entries_api, name='kardex_api'),
]
