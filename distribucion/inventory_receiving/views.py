from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from distribution.decorators import role_required
from .models import ProductReception
from .forms import ProductReceptionForm


# ---------------- LIST ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'warehouse_staff', 'inventory_controller', 'viewer'])
def reception_list(request):
    receptions = ProductReception.objects.all()
    return render(request, 'inventory_reception/list.html', {'receptions': receptions})


# ---------------- CREATE ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'warehouse_staff', 'inventory_controller'])
def reception_create(request):
    if request.method == 'POST':
        form = ProductReceptionForm(request.POST)
        if form.is_valid():
            reception = form.save(commit=False)
            reception.receiver = request.user

            # Si hay viaje, obtener la cantidad desde TripProduct
            if reception.trip:
                trip_product = reception.trip.products.filter(product=reception.product).first()
                if trip_product:
                    reception.quantity_received = trip_product.quantity
                    # Cambiar estado del viaje
                    reception.trip.status = 'completed'
                    reception.trip.save()
                else:
                    messages.error(request, "No se encontró el producto en el viaje seleccionado.")
                    return render(request, 'inventory_reception/form.html', {'form': form})

            # Validación extra
            if not reception.quantity_received:
                messages.error(request, "Debe ingresar una cantidad recibida.")
                return render(request, 'inventory_reception/form.html', {'form': form})

            reception.save()
            messages.success(request, "Recepción registrada correctamente.")
            return redirect('inventory_receiving:reception_list')
        else:
            print("❌ Formulario inválido:", form.errors)
    else:
        form = ProductReceptionForm()

    return render(request, 'inventory_reception/form.html', {'form': form})


# ---------------- UPDATE ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'warehouse_staff', 'inventory_controller'])
def reception_update(request, pk):
    reception = get_object_or_404(ProductReception, pk=pk)
    if request.method == 'POST':
        form = ProductReceptionForm(request.POST, instance=reception)
        if form.is_valid():
            form.save()
            messages.success(request, "Recepción actualizada correctamente.")
            return redirect('inventory_receiving:reception_list')
    else:
        form = ProductReceptionForm(instance=reception)
    return render(request, 'inventory_reception/form.html', {'form': form})


# ---------------- DELETE ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'warehouse_staff', 'inventory_controller'])
def reception_delete(request, pk):
    reception = get_object_or_404(ProductReception, pk=pk)
    if request.method == 'POST':
        reception.delete()
        messages.success(request, "Recepción eliminada correctamente.")
        return redirect('inventory_receiving:reception_list')
    return render(request, 'inventory_reception/delete_confirm.html', {'object': reception})
