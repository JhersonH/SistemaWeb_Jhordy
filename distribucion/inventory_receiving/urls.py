from django.urls import path
from . import views

app_name = 'inventory_receiving'

urlpatterns = [
    path('', views.reception_list, name='reception_list'),
    path('crear/', views.reception_create, name='reception_create'),
    path('<int:pk>/editar/', views.reception_update, name='reception_update'),
    path('<int:pk>/eliminar/', views.reception_delete, name='reception_delete'),
]
