from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import *

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'transport/vehicle_list.html'

class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'transport/vehicle_form.html'
    success_url = reverse_lazy('transport:vehicle_list')

class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'transport/vehicle_form.html'
    success_url = reverse_lazy('transport:vehicle_list')

class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'transport/vehicle_confirm_delete.html'
    success_url = reverse_lazy('transport:vehicle_list')

def driver_list(request):
    drivers = Driver.objects.select_related('user')
    return render(request, 'transport/driver_list.html', {'drivers': drivers})

def driver_create(request):
    form = DriverForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('transport:driver_list')
    return render(request, 'transport/driver_form.html', {'form': form, 'title': 'Nuevo Conductor'})

def driver_update(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    form = DriverForm(request.POST or None, instance=driver)
    if form.is_valid():
        form.save()
        return redirect('transport:driver_list')
    return render(request, 'transport/driver_form.html', {'form': form, 'title': 'Editar Conductor'})

def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        driver.delete()
        return redirect('transport:driver_list')
    return render(request, 'transport/driver_confirm_delete.html', {'driver': driver})

def route_list(request):
    routes = Route.objects.all()
    return render(request, 'transport/route_list.html', {'routes': routes})

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

def route_delete(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        route.delete()
        messages.success(request, 'Ruta eliminada.')
        return redirect('transport:route_list')
    return render(request, 'transport/route_confirm_delete.html', {'route': route})

def trip_list(request):
    trips = Trip.objects.select_related("route", "vehicle", "driver").all()
    return render(request, "transport/trip/list.html", {"trips": trips})

def trip_create(request):
    form = TripForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Viaje creado correctamente.")
        return redirect("transport:trip_list")
    return render(request, "transport/trip/form.html", {"form": form, "title": "Nuevo viaje"})

def trip_update(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    form = TripForm(request.POST or None, instance=trip)
    if form.is_valid():
        form.save()
        messages.success(request, "Viaje actualizado correctamente.")
        return redirect("transport:trip_list")
    return render(request, "transport/trip/form.html", {"form": form, "title": f"Editar {trip.code}"})

def trip_delete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == "POST":
        trip.delete()
        messages.success(request, "Viaje eliminado.")
        return redirect("transport:trip_list")
    return render(request, "transport/trip/delete_confirm.html", {"trip": trip})

def stop_list_all(request):
    trips = Trip.objects.all()
    return render(request, 'transport/stops/list.html', {
        'trips': trips,
        'selected_trip_id': None,
        'trip': None,
        'stops': None,
    })

def stop_list_by_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    stops = trip.stops.all()
    trips = Trip.objects.all()
    return render(request, 'transport/stops/list.html', {
        'trips': trips,
        'selected_trip_id': trip.id,
        'trip': trip,
        'stops': stops,
    })

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

def stop_delete(request, pk):
    stop = get_object_or_404(Stop, pk=pk)
    trip_id = stop.trip.id
    stop.delete()
    messages.success(request, "Punto de parada eliminado.")
    return redirect("transport:stop_list", trip_id=trip_id)

def expense_list(request):
    expenses = Expense.objects.select_related('trip').order_by('-created_at')
    return render(request, 'transport/expense/list.html', {'expenses': expenses})

def expense_create(request):
    form = ExpenseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Gasto registrado correctamente.")
        return redirect('transport:expense_list')
    return render(request, 'transport/expense/form.html', {'form': form, 'title': 'Registrar gasto'})

def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseForm(request.POST or None, request.FILES or None, instance=expense)
    if form.is_valid():
        form.save()
        messages.success(request, "Gasto actualizado.")
        return redirect('transport:expense_list')
    return render(request, 'transport/expense/form.html', {'form': form, 'title': 'Editar gasto'})

def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Gasto eliminado.")
        return redirect('transport:expense_list')
    return render(request, 'transport/expense/confirm_delete.html', {'expense': expense})

def incident_list(request):
    incidents = Incident.objects.select_related('trip').order_by('-occurred_at')
    return render(request, 'transport/incidents/list.html', {'incidents': incidents})

def incident_create(request):
    form = IncidentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Incidente registrado correctamente.")
        return redirect('transport:incident_list')
    return render(request, 'transport/incidents/form.html', {'form': form, 'title': 'Registrar incidente'})

def incident_update(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    form = IncidentForm(request.POST or None, request.FILES or None, instance=incident)
    if form.is_valid():
        form.save()
        messages.success(request, "Incidente actualizado correctamente.")
        return redirect('transport:incident_list')
    return render(request, 'transport/incidents/form.html', {'form': form, 'title': 'Editar incidente'})

def incident_delete(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    if request.method == 'POST':
        incident.delete()
        messages.success(request, "Incidente eliminado.")
        return redirect('transport:incident_list')
    return render(request, 'transport/incidents/confirm_delete.html', {'object': incident})
