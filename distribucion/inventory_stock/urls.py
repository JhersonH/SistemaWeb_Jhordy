# inventory_stock/urls.py

from django.urls import path
from . import views

app_name = 'inventory_stock'

urlpatterns = [
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/create/', views.stock_create, name='stock_create'),
    path('stock/edit/<int:pk>/', views.stock_edit, name='stock_update'),
    path('stock/delete/<int:pk>/', views.stock_delete, name='stock_delete'),

    path('ubicaciones/', views.location_list, name='location_list'),
    path('ubicaciones/create/', views.location_create, name='location_create'),
    path('ubicaciones/edit/<int:pk>/', views.location_update, name='location_update'),
    path('ubicaciones/delete/<int:pk>/', views.location_delete, name='location_delete'),
]
