# users/urls.py
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.user_list, name="list"),
    path("create/", views.user_create, name="create"),
    path("<int:pk>/edit/", views.user_update, name="update"),
    path("<int:pk>/toggle-active/", views.user_toggle_active, name="toggle_active"),
    path("<int:pk>/reset-password/", views.user_reset_password, name="reset_password"),
    path("empleados/", views.employee_list, name="employee_list"),
    path("empleados/<int:pk>/editar/", views.employee_update, name="employee_update"),
    path("perfil/", views.profile_update, name="profile_update"),
]
