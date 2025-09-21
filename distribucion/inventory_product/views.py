from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from distribution.decorators import role_required


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory_product/product_list.html', {'products': products})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inventory_product:product_list')
    return render(request, 'inventory_product/product_form.html', {'form': form})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('inventory_product:product_list')
    return render(request, 'inventory_product/product_form.html', {'form': form})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('inventory_product:product_list')
    return render(request, 'inventory_product/product_confirm_delete.html', {'product': product})
