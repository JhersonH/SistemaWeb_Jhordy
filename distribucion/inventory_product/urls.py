# inventory_product/urls.py
from django.urls import path
from . import views

app_name = 'inventory_product'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('edit/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
]
