from django.urls import path
from . import views

app_name = 'inventory_adjustments'

urlpatterns = [
    path('', views.adjustment_list, name='adjustment_list'),
    path('create/', views.adjustment_create, name='adjustment_create'),
    path('<int:pk>/update/', views.adjustment_update, name='adjustment_update'),
    path('<int:pk>/delete/', views.adjustment_delete, name='adjustment_delete'),
]
