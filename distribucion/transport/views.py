from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from distribution.decorators import role_required
from .forms import *
from .models import Vehicle, Driver, Route, Trip, Stop, Expense, Incident, VehicleModel, VehicleBrand, StockLocation
from django.http import JsonResponse

import json
import os
from django.conf import settings

# ---------------- VEHICLES ----------------
@method_decorator([login_required, role_required(['ops_manager', 'warehouse_manager', 'viewer'])], name='dispatch')
class VehicleListView(ListView):
    model = Vehicle
    template_name = 'transport/vehicle_list.html'


@method_decorator([login_required, role_required(['ops_manager', 'warehouse_manager'])], name='dispatch')
class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'transport/vehicle_form.html'
    success_url = reverse_lazy('transport:vehicle_list')


@method_decorator([login_required, role_required(['ops_manager', 'warehouse_manager'])], name='dispatch')
class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'transport/vehicle_form.html'
    success_url = reverse_lazy('transport:vehicle_list')


@method_decorator([login_required, role_required(['ops_manager', 'warehouse_manager'])], name='dispatch')
class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'transport/vehicle_confirm_delete.html'
    success_url = reverse_lazy('transport:vehicle_list')

@login_required
def load_vehicle_models(request):
    brand_id = request.GET.get("brand_id")
    if not brand_id:
        return JsonResponse([], safe=False)

    models = VehicleModel.objects.filter(brand_id=brand_id).order_by("name")
    model_list = [{"id": m.id, "name": m.name} for m in models]
    return JsonResponse(model_list, safe=False)

@login_required
def ajax_brand_autocomplete(request):
    term = request.GET.get("q", "")
    brands = VehicleBrand.objects.filter(name__icontains=term).order_by("name")
    results = [{"id": b.id, "text": b.name} for b in brands]
    return JsonResponse({"results": results})

@login_required
def ajax_model_autocomplete(request):
    term = request.GET.get("q", "")
    brand_id = request.GET.get("brand_id")

    qs = VehicleModel.objects.all()
    if brand_id:
        qs = qs.filter(brand_id=brand_id)

    models = qs.filter(name__icontains=term).order_by("name")
    results = [{"id": m.id, "text": m.name} for m in models]
    return JsonResponse({"results": results})

# ---------------- DRIVERS ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'viewer'])
def driver_list(request):
    drivers = Driver.objects.select_related('user')
    return render(request, 'transport/driver_list.html', {'drivers': drivers})


@login_required
@role_required(['ops_manager', 'warehouse_manager'])
def driver_create(request):
    form = DriverForm(request.POST or None)
    if form.is_valid():
        user = form.cleaned_data['user']

        if not hasattr(user, 'profile') or not user.profile.role or user.profile.role.role_type != 'driver':
            form.add_error('user', 'El usuario seleccionado no tiene rol de conductor.')
        else:
            form.save()
            return redirect('transport:driver_list')
    return render(request, 'transport/driver_form.html', {'form': form, 'title': 'Nuevo Conductor'})


@login_required
@role_required(['ops_manager', 'warehouse_manager'])
def driver_update(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    form = DriverForm(request.POST or None, instance=driver)
    if form.is_valid():
        form.save()
        return redirect('transport:driver_list')
    return render(request, 'transport/driver_form.html', {'form': form, 'title': 'Editar Conductor'})


@login_required
@role_required(['ops_manager', 'warehouse_manager'])
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        driver.delete()
        return redirect('transport:driver_list')
    return render(request, 'transport/driver_confirm_delete.html', {'driver': driver})


# ---------------- ROUTES ----------------
@login_required
@role_required(['ops_manager', 'dispatcher', 'driver', 'viewer'])
def route_list(request):
    routes = Route.objects.all()
    return render(request, 'transport/route_list.html', {'routes': routes})


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def route_create(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ruta creada correctamente.')
            return redirect('transport:route_list')
    else:
        form = RouteForm()
    return render(request, 'transport/route_form.html', {'form': form, 'title': 'Crear Ruta'})


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def route_update(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ruta actualizada.')
            return redirect('transport:route_list')
    else:
        form = RouteForm(instance=route)
    return render(request, 'transport/route_form.html', {'form': form, 'title': 'Editar Ruta'})


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def route_delete(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        route.delete()
        messages.success(request, 'Ruta eliminada.')
        return redirect('transport:route_list')
    return render(request, 'transport/route_confirm_delete.html', {'route': route})


# ---------------- TRIPS ----------------
@login_required
@role_required(['ops_manager', 'dispatcher', 'driver', 'viewer'])
def trip_list(request):
    trips = Trip.objects.select_related("route", "vehicle", "driver").all()
    return render(request, "transport/trip/list.html", {"trips": trips})


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        formset = TripProductFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            trip = form.save()
            formset.instance = trip
            formset.save()
            messages.success(request, "Viaje creado correctamente con productos.")
            return redirect("transport:trip_list")
    else:
        form = TripForm()
        formset = TripProductFormSet()
    return render(request, "transport/trip/form.html", {
        "form": form,
        "formset": formset,
        "title": "Nuevo viaje",
        "is_create": True
    })


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def trip_update(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    form = TripForm(request.POST or None, instance=trip)
    if form.is_valid():
        form.save()
        messages.success(request, "Viaje actualizado correctamente.")
        return redirect("transport:trip_list")
    return render(request, "transport/trip/form.html", {
        "form": form,
        "title": f"Editar {trip.code}",
        "trip": trip,
        "is_create": False
    })


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == "POST":
        trip.delete()
        messages.success(request, "Viaje eliminado.")
        return redirect("transport:trip_list")
    return render(request, "transport/trip/delete_confirm.html", {"trip": trip})


# ---------------- STOPS ----------------
@login_required
@role_required(['ops_manager', 'dispatcher', 'driver', 'viewer'])
def stop_list_all(request):
    trips = Trip.objects.all()
    return render(request, 'transport/stops/list.html', {
        'trips': trips, 'selected_trip_id': None, 'trip': None, 'stops': None,
    })


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver', 'viewer'])
def stop_list_by_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    stops = trip.stops.all()
    trips = Trip.objects.all()
    return render(request, 'transport/stops/list.html', {
        'trips': trips, 'selected_trip_id': trip.id, 'trip': trip, 'stops': stops,
    })


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def stop_create(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        form = StopForm(request.POST, request.FILES)
        if form.is_valid():
            stop = form.save(commit=False)
            stop.trip = trip
            stop.save()
            messages.success(request, "Punto de parada creado correctamente.")
            return redirect("transport:stop_list", trip_id=trip.id)
    else:
        form = StopForm()
    return render(request, "transport/stops/form.html", {"form": form, "trip": trip})


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def stop_update(request, pk):
    stop = get_object_or_404(Stop, pk=pk)
    if request.method == "POST":
        form = StopForm(request.POST, request.FILES, instance=stop)
        if form.is_valid():
            form.save()
            messages.success(request, "Punto de parada actualizado correctamente.")
            return redirect("transport:stop_list", trip_id=stop.trip.id)
    else:
        form = StopForm(instance=stop)
    return render(request, "transport/stops/form.html", {"form": form, "trip": stop.trip, "is_create": False})


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def stop_delete(request, pk):
    stop = get_object_or_404(Stop, pk=pk)
    trip_id = stop.trip.id
    stop.delete()
    messages.success(request, "Punto de parada eliminado.")
    return redirect("transport:stop_list", trip_id=trip_id)


# ---------------- EXPENSES ----------------
@login_required
@role_required(['ops_manager'])
def expense_list(request):
    expenses = Expense.objects.select_related('trip').order_by('-created_at')
    return render(request, 'transport/expense/list.html', {'expenses': expenses})


@login_required
@role_required(['ops_manager'])
def expense_create(request):
    form = ExpenseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Gasto registrado correctamente.")
        return redirect('transport:expense_list')
    return render(request, 'transport/expense/form.html', {'form': form, 'title': 'Registrar gasto'})


@login_required
@role_required(['ops_manager'])
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseForm(request.POST or None, request.FILES or None, instance=expense)
    if form.is_valid():
        form.save()
        messages.success(request, "Gasto actualizado.")
        return redirect('transport:expense_list')
    return render(request, 'transport/expense/form.html', {'form': form, 'title': 'Editar gasto'})


@login_required
@role_required(['ops_manager'])
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Gasto eliminado.")
        return redirect('transport:expense_list')
    return render(request, 'transport/expense/confirm_delete.html', {'expense': expense})


# ---------------- INCIDENTS ----------------
@login_required
@role_required(['ops_manager', 'dispatcher', 'driver', 'viewer'])
def incident_list(request):
    incidents = Incident.objects.select_related('trip').order_by('-occurred_at')
    return render(request, 'transport/incidents/list.html', {'incidents': incidents})


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def incident_create(request):
    form = IncidentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Incidente registrado correctamente.")
        return redirect('transport:incident_list')
    return render(request, 'transport/incidents/form.html', {'form': form, 'title': 'Registrar incidente'})


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def incident_update(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    form = IncidentForm(request.POST or None, request.FILES or None, instance=incident)
    if form.is_valid():
        form.save()
        messages.success(request, "Incidente actualizado correctamente.")
        return redirect('transport:incident_list')
    return render(request, 'transport/incidents/form.html', {'form': form, 'title': 'Editar incidente'})


@login_required
@role_required(['ops_manager', 'dispatcher', 'driver'])
def incident_delete(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    if request.method == 'POST':
        incident.delete()
        messages.success(request, "Incidente eliminado.")
        return redirect('transport:incident_list')
    return render(request, 'transport/incidents/confirm_delete.html', {'object': incident})

@login_required
def load_vehicle_data_by_plate(request):
    """
    Vista que devuelve el JSON de vehículos filtrado por placa.
    Útil para autocompletado basado en placa.
    """
    json_path = os.path.join(settings.BASE_DIR, 'transport', 'vehicle_api.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return JsonResponse({"error": "Archivo vehicle_api.json no encontrado."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Error al leer el archivo JSON."}, status=500)

    placa = request.GET.get("placa", "").strip().upper()
    if placa:
        vehiculo = data.get(placa)
        if vehiculo:
            return JsonResponse(vehiculo)
        else:
            return JsonResponse({"error": "Placa no encontrada"}, status=404)

    return JsonResponse(data)

@login_required
def load_driver_data_by_user(request):
    """
    Vista que devuelve datos del conductor por username.
    Útil para autocompletado basado en usuario.
    """
    json_path = os.path.join(settings.BASE_DIR, 'transport', 'driver_api.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return JsonResponse({"error": "Archivo driver_api.json no encontrado."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Error al leer el archivo JSON."}, status=500)

    username = request.GET.get("username", "").strip()
    if username:
        conductor = data.get(username)
        if conductor:
            return JsonResponse(conductor)
        else:
            return JsonResponse({"error": "Usuario no encontrado en la base de datos."}, status=404)

    return JsonResponse(data)

@login_required
def load_route_data_by_locations(request):
    """
    Vista que devuelve la distancia y ETA entre origen y destino.
    Útil para autocompletado basado en ubicaciones.
    """
    json_path = os.path.join(settings.BASE_DIR, 'transport', 'route_distances.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return JsonResponse({"error": "Archivo route_distances.json no encontrado."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Error al leer el archivo JSON."}, status=500)

    origin_id = request.GET.get("origin", "").strip()
    destination_id = request.GET.get("destination", "").strip()

    if not origin_id or not destination_id:
        return JsonResponse({"error": "Faltan parámetros 'origin' o 'destination'."}, status=400)

    try:
        origin_obj = StockLocation.objects.get(id=origin_id)
        destination_obj = StockLocation.objects.get(id=destination_id)
    except StockLocation.DoesNotExist:
        return JsonResponse({"error": "Origen o destino no encontrado."}, status=404)

    origin_name = origin_obj.name
    destination_name = destination_obj.name

    # Crear clave como "Origin - Destination"
    key = f"{origin_name} - {destination_name}"

    # Buscar también en reversa si no encuentra
    reverse_key = f"{destination_name} - {origin_name}"
    route_data = data.get(key) or data.get(reverse_key)

    if route_data:
        return JsonResponse(route_data)
    else:
        return JsonResponse({
            "distance_km": 0,
            "eta_minutes": 0
        })