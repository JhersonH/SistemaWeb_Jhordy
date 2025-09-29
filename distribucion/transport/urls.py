from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('ajax/load-vehicle-models/', views.load_vehicle_models, name='ajax_load_vehicle_models'),
    path('ajax/autocomplete/brand/', views.ajax_brand_autocomplete, name='ajax_brand_autocomplete'),
    path('ajax/autocomplete/model/', views.ajax_model_autocomplete, name='ajax_model_autocomplete'),

    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/new/', views.driver_create, name='driver_create'),
    path('drivers/<int:pk>/edit/', views.driver_update, name='driver_update'),
    path('drivers/<int:pk>/delete/', views.driver_delete, name='driver_delete'),

    path('routes/', views.route_list, name='route_list'),
    path('routes/create/', views.route_create, name='route_create'),
    path('routes/<int:pk>/edit/', views.route_update, name='route_update'),
    path('routes/<int:pk>/delete/', views.route_delete, name='route_delete'),

    path("trips/", views.trip_list, name="trip_list"),
    path("trips/create/", views.trip_create, name="trip_create"),
    path("trips/<int:pk>/edit/", views.trip_update, name="trip_update"),
    path("trips/<int:pk>/delete/", views.trip_delete, name="trip_delete"),

    path('trips/<int:trip_id>/stops/create/', views.stop_create, name="stop_create"),
    path('stops/<int:pk>/edit/', views.stop_update, name="stop_update"),
    path('stops/<int:pk>/delete/', views.stop_delete, name="stop_delete"),

    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    path('expenses/<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),

    path("incidents/", views.incident_list, name="incident_list"),
    path("incidents/new/", views.incident_create, name="incident_create"),
    path("incidents/<int:pk>/edit/", views.incident_update, name="incident_update"),
    path("incidents/<int:pk>/delete/", views.incident_delete, name="incident_delete"),

    path('stops/', views.stop_list_all, name='stop_list_all'),
    path('trips/<int:trip_id>/stops/', views.stop_list_by_trip, name='stop_list'),
]
