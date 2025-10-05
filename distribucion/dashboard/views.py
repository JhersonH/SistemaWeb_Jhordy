from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta, datetime
import unicodedata
from inventory_adjustments.models import InventoryAdjustment
from django.utils.timezone import make_aware, localtime
from django.db.models.functions import TruncMonth
import calendar
from collections import Counter

# Modelos
from transport.models import Vehicle, Trip
from inventory_product.models import Product, ProductCategory
from inventory_movements.models import InventoryMovement
from inventory_stock.models import ProductStock
from transport.models import Driver
from transport.models import TripProduct
from users.models import Profile
from roles.models import Role

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrecta.")
        return super().form_invalid(form)


@login_required
def dashboard(request):
    """Dashboard dinámico según el rol del usuario."""
    user = request.user
    profile = getattr(user, "profile", None)
    role_obj = getattr(profile, "role", None)
    role = str(role_obj) if role_obj else None

    print("DEBUG ROLE:", role)

    # Variables para Chart.js
    courses_levels_labels = []
    courses_levels_data = []
    documents_types_labels = []
    documents_types_data = []
    stock_min_data = []
    schedules_labels = []
    schedules_data = []
    hours_per_day_data = []

    # Traducción de días (clave para todos los roles)
    day_translation = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }

    if request.user.is_superuser:
        print("✅ Entrando al bloque del rol Administrador / Superusuario")

        # 1️⃣ Vehículos por estado
        vehicles_by_status = Vehicle.objects.values("status").annotate(total=Count("id"))
        status_map = dict(Vehicle.STATUS_CHOICES)
        vehicles_labels = [status_map.get(v["status"], v["status"]) for v in vehicles_by_status]
        vehicles_data = [v["total"] for v in vehicles_by_status]

        # 2️⃣ Stock vs. Alertas de mínimo
        stocks = ProductStock.objects.select_related("product", "location")
        stock_total = stocks.aggregate(total=Sum("quantity"))["total"] or 0
        alerts_total = sum(1 for s in stocks if s.quantity < s.product.min_stock)

        stock_vs_min_labels = ["Stock Actual", "Productos en Alerta"]
        stock_vs_min_data = [stock_total, alerts_total]

        # 3️⃣ Viajes y transporte por día (últimos 7 días)
        today = timezone.now().date()
        last_week = today - timedelta(days=6)
        trips_last_week = Trip.objects.filter(date__range=[last_week, today])

        trips_counter = Counter([trip.date.strftime("%A") for trip in trips_last_week])
        day_translation = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo",
        }
        schedules_labels = list(day_translation.values())
        schedules_data = [trips_counter.get(day, 0) for day in day_translation]

        # 4️⃣ Usuarios por rol
        users_by_role = Profile.objects.values("role__role_type").annotate(total=Count("id"))
        role_map = dict(Role.ROLE_CHOICES)

        users_labels = []
        users_data = []

        for u in users_by_role:
            role_key = u["role__role_type"]
            if role_key:
                label = role_map.get(role_key, role_key)  # Traduce con ROLE_CHOICES
            else:
                label = "Sin rol"
            users_labels.append(label)
            users_data.append(u["total"])

        # Evita que quede vacío
        if not users_labels:
            users_labels = ["Sin datos"]
            users_data = [1]

        print("DEBUG Usuarios por rol:", users_labels, users_data)  # 👈 Debug

        # 5️⃣ Viajes por estado (para "Transportes por Día")
        trips_by_status = Trip.objects.values("status").annotate(total=Count("id"))
        status_map_trips = dict(Trip.STATUS)
        hours_per_day_labels = [status_map_trips.get(t["status"], t["status"]) for t in trips_by_status]
        hours_per_day_data = [t["total"] for t in trips_by_status]

        # ✅ Contexto
        context = {
            "debug_role": "Administrador",
            # Resumen general (vehículos por estado)
            "courses_levels_labels": vehicles_labels,
            "courses_levels_data": vehicles_data,
            # Stock vs alertas
            "documents_types_labels": stock_vs_min_labels,
            "documents_types_data": stock_vs_min_data,
            # Viajes y transporte por día
            "schedules_labels": schedules_labels,
            "schedules_data": schedules_data,
            # Usuarios por rol
            "users_labels": users_labels,
            "users_data": users_data,
            # Viajes por estado (nuevo dataset)
            "hours_per_day_data": hours_per_day_data,
            "hours_per_day_labels": hours_per_day_labels,
        }
        return render(request, "dashboard/home.html", context)

    # Rol: Jefe de Operaciones
    elif normalize_string(role) == "jefe de operaciones":
        print("✅ Entrando al bloque del rol Jefe de Operaciones")

        vehicles_by_status = Vehicle.objects.values('status').annotate(count=Count('id')).order_by('status')
        status_map = dict(Vehicle.STATUS_CHOICES)
        courses_levels_labels = [status_map.get(v['status'], v['status']) for v in vehicles_by_status]
        courses_levels_data = [v['count'] for v in vehicles_by_status]

        categories = ProductCategory.objects.all()
        documents_types_labels = [c.name for c in categories]
        documents_types_data = [Product.objects.filter(category=c).count() for c in categories]

        today = timezone.now().date()
        last_week = today - timedelta(days=6)
        trips = Trip.objects.filter(date__range=[last_week, today])

        trips_counter = Counter([day_translation[d.strftime('%A')] for d in trips.values_list('date', flat=True)])

        schedules_labels = list(day_translation.values())
        schedules_data = [trips_counter.get(day, 0) for day in schedules_labels]
        hours_per_day_data = [count * 60 for count in schedules_data]

    # Rol: Despachador
    elif normalize_string(role) == "despachador":
        print("✅ Entrando al bloque del rol Despachador")

        trips_by_status = (
            Trip.objects.values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )
        status_map = dict(Trip.STATUS) if hasattr(Trip, "STATUS") else {
            "planned": "Pendiente",
            "in_progress": "En curso",
            "finished": "Finalizado",
        }
        courses_levels_labels = [status_map.get(item["status"], item["status"]) for item in trips_by_status]
        courses_levels_data = [item["total"] for item in trips_by_status]

        active_drivers = Driver.objects.filter(active=True).count()
        inactive_drivers = Driver.objects.filter(active=False).count()
        documents_types_labels = ["Activos", "Inactivos"]
        documents_types_data = [active_drivers, inactive_drivers]

        today = timezone.now().date()
        last_week = today - timedelta(days=6)
        trips_last_week = Trip.objects.filter(date__range=[last_week, today])

        trips_counter = Counter([day_translation[trip.date.strftime("%A")] for trip in trips_last_week])

        schedules_labels = list(day_translation.values())
        schedules_data = [trips_counter.get(day, 0) for day in schedules_labels]

        context = {
            "debug_role": role,
            "courses_levels_labels": courses_levels_labels,
            "courses_levels_data": courses_levels_data,
            "active_drivers": active_drivers,
            "inactive_drivers": inactive_drivers,
            "documents_types_labels": documents_types_labels,
            "documents_types_data": documents_types_data,
            "schedules_labels": schedules_labels,
            "schedules_data": schedules_data,
        }
        return render(request, "dashboard/home.html", context)

    # Rol: Consulta / Solo Lectura
    elif normalize_string(role) == "consulta / solo lectura":
        print("✅ Entrando al bloque del rol Consulta / Solo Lectura")

        stock_by_category = (
            Product.objects
            .values("category__name")
            .annotate(total=Sum("stocks__quantity"))
            .order_by("category__name")
        )
        courses_levels_labels = [item["category__name"] or "Sin categoría" for item in stock_by_category]
        courses_levels_data = [item["total"] or 0 for item in stock_by_category]

        today = timezone.now().date()
        last_week = today - timedelta(days=6)
        trips_last_week = Trip.objects.filter(date__range=[last_week, today])

        trips_counter = Counter([day_translation[trip.date.strftime("%A")] for trip in trips_last_week])

        schedules_labels = list(day_translation.values())
        schedules_data = [trips_counter.get(day, 0) for day in schedules_labels]

        top_products = (
            InventoryMovement.objects
            .values("product__name")
            .annotate(total=Sum("quantity"))
            .order_by("-total")[:5]
        )
        top_products_labels = [p["product__name"] for p in top_products]
        top_products_data = [p["total"] for p in top_products]

        context = {
            "debug_role": role,
            "courses_levels_labels": courses_levels_labels,
            "courses_levels_data": courses_levels_data,
            "schedules_labels": schedules_labels,
            "schedules_data": schedules_data,
            "top_products_labels": top_products_labels,
            "top_products_data": top_products_data,
        }
        return render(request, "dashboard/home.html", context)

    else:
        print("⚠️ Rol no reconocido o sin datos asignados")

    context = {
        "debug_role": role,
        "courses_levels_labels": courses_levels_labels,
        "courses_levels_data": courses_levels_data,
        "documents_types_labels": documents_types_labels,
        "documents_types_data": documents_types_data,
        "stock_min_data": stock_min_data,
        "schedules_labels": schedules_labels,
        "schedules_data": schedules_data,
        "hours_per_day_data": hours_per_day_data,
    }

    return render(request, 'dashboard/home.html', context)


def normalize_string(value):
    if not isinstance(value, str):
        value = str(value)
    return ''.join(
        c for c in unicodedata.normalize('NFD', value)
        if unicodedata.category(c) != 'Mn'
    ).lower()


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'dashboard/change_password.html'
    success_url = reverse_lazy('teacher_profile')

    def form_valid(self, form):
        messages.success(self.request, _('Tu contraseña ha sido actualizada correctamente.'))
        return super().form_valid(form)


def custom_permission_denied_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)