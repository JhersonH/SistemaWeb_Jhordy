from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from distribution.decorators import role_required
from .models import InventoryMovement
from .forms import InventoryMovementForm


# ---------------- LIST ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'warehouse_staff', 'inventory_controller', 'viewer'])
def movement_list(request):
    movements = InventoryMovement.objects.all().order_by('-date')
    return render(request, 'inventory_movements/list.html', {'movements': movements})


# ---------------- CREATE ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'warehouse_staff', 'inventory_controller'])
def movement_create(request):
    if request.method == 'POST':
        form = InventoryMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.registered_by = request.user
            movement.save()
            messages.success(request, "Movimiento registrado correctamente.")
            return redirect('inventory_movements:movement_list')
    else:
        form = InventoryMovementForm()
    return render(request, 'inventory_movements/form.html', {'form': form})


# ---------------- UPDATE ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'warehouse_staff', 'inventory_controller'])
def movement_update(request, pk):
    movement = get_object_or_404(InventoryMovement, pk=pk)
    form = InventoryMovementForm(request.POST or None, instance=movement)
    if form.is_valid():
        form.save()
        messages.success(request, "Movimiento actualizado correctamente.")
        return redirect('inventory_movements:movement_list')
    return render(request, 'inventory_movements/form.html', {'form': form})


# ---------------- DELETE ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'warehouse_staff', 'inventory_controller'])
def movement_delete(request, pk):
    movement = get_object_or_404(InventoryMovement, pk=pk)
    if request.method == 'POST':
        movement.delete()
        messages.success(request, "Movimiento eliminado correctamente.")
        return redirect('inventory_movements:movement_list')
    return render(request, 'inventory_movements/delete_confirm.html', {'object': movement})
