from django.urls import path
from . import views

app_name = 'inventory_movements'

urlpatterns = [
    path('', views.movement_list, name='movement_list'),
    path('crear/', views.movement_create, name='movement_create'),
    path('editar/<int:pk>/', views.movement_update, name='movement_update'),
    path('eliminar/<int:pk>/', views.movement_delete, name='movement_delete'),
]
