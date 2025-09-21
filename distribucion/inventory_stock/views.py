from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from distribution.decorators import role_required
from .models import ProductStock, StockLocation
from .forms import ProductStockForm, StockLocationForm


# ------------------ STOCK ------------------

@login_required
def stock_list(request):
    stocks = ProductStock.objects.select_related('product', 'location')
    return render(request, 'inventory_stock/list.html', {'stocks': stocks})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def stock_create(request):
    form = ProductStockForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Stock creado correctamente.")
        return redirect('inventory_stock:stock_list')
    return render(request, 'inventory_stock/form.html', {'form': form, 'title': 'Nuevo Stock'})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def stock_edit(request, pk):
    stock = get_object_or_404(ProductStock, pk=pk)
    form = ProductStockForm(request.POST or None, instance=stock)
    if form.is_valid():
        form.save()
        messages.success(request, "Stock actualizado correctamente.")
        return redirect('inventory_stock:stock_list')
    return render(request, 'inventory_stock/form.html', {'form': form, 'title': 'Editar Stock'})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def stock_delete(request, pk):
    stock = get_object_or_404(ProductStock, pk=pk)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, "Stock eliminado correctamente.")
        return redirect('inventory_stock:stock_list')
    return render(request, 'inventory_stock/delete_confirm.html', {'object': stock})


# ------------------ LOCATIONS ------------------

@login_required
def location_list(request):
    locations = StockLocation.objects.all()
    return render(request, 'inventory_stock/location_list.html', {'locations': locations, 'title': 'Ubicaciones de Stock'})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def location_create(request):
    form = StockLocationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inventory_stock:location_list')
    return render(request, 'inventory_stock/location_form.html', {'form': form, 'title': 'Agregar Ubicación'})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def location_update(request, pk):
    location = get_object_or_404(StockLocation, pk=pk)
    form = StockLocationForm(request.POST or None, instance=location)
    if form.is_valid():
        form.save()
        return redirect('inventory_stock:location_list')
    return render(request, 'inventory_stock/location_form.html', {'form': form, 'title': 'Editar Ubicación'})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def location_delete(request, pk):
    location = get_object_or_404(StockLocation, pk=pk)
    if request.method == 'POST':
        location.delete()
        messages.success(request, "Ubicación eliminada correctamente.")
        return redirect('inventory_stock:location_list')
    return render(request, 'inventory_stock/location_confirm_delete.html', {'object': location, 'title': 'Eliminar Ubicación'})
