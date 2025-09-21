from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from distribution.decorators import role_required
from .models import InventoryAdjustment
from .forms import InventoryAdjustmentForm


# ---------------- LIST ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller', 'viewer'])
def adjustment_list(request):
    adjustments = InventoryAdjustment.objects.all()
    return render(request, 'inventory_adjustments/list.html', {'adjustments': adjustments})


# ---------------- CREATE ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def adjustment_create(request):
    if request.method == 'POST':
        form = InventoryAdjustmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajuste registrado correctamente.")
            return redirect('inventory_adjustments:adjustment_list')
    else:
        form = InventoryAdjustmentForm()
    return render(request, 'inventory_adjustments/form.html', {'form': form})


# ---------------- UPDATE ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def adjustment_update(request, pk):
    adjustment = get_object_or_404(InventoryAdjustment, pk=pk)
    if request.method == 'POST':
        form = InventoryAdjustmentForm(request.POST, instance=adjustment)
        if form.is_valid():
            form.save()
            messages.success(request, "Ajuste actualizado correctamente.")
            return redirect('inventory_adjustments:adjustment_list')
    else:
        form = InventoryAdjustmentForm(instance=adjustment)
    return render(request, 'inventory_adjustments/form.html', {'form': form})


# ---------------- DELETE ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def adjustment_delete(request, pk):
    adjustment = get_object_or_404(InventoryAdjustment, pk=pk)
    if request.method == 'POST':
        adjustment.delete()
        messages.success(request, "Ajuste eliminado correctamente.")
        return redirect('inventory_adjustments:adjustment_list')
    return render(request, 'inventory_adjustments/delete_confirm.html', {'adjustment': adjustment})
