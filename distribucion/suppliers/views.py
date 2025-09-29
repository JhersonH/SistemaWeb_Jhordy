from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from distribution.decorators import role_required
from .models import Supplier
from .forms import SupplierForm


# ---------------- SUPPLIERS ----------------
@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/list.html", {"suppliers": suppliers})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def supplier_create(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Proveedor registrado correctamente.")
        return redirect("suppliers:supplier_list")
    return render(request, "suppliers/form.html", {"form": form, "title": "Nuevo Proveedor"})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if form.is_valid():
        form.save()
        messages.success(request, "Proveedor actualizado correctamente.")
        return redirect("suppliers:supplier_list")
    return render(request, "suppliers/form.html", {"form": form, "title": "Editar Proveedor"})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect("suppliers:supplier_list")
    return render(request, "suppliers/delete_confirm.html", {"supplier": supplier})
