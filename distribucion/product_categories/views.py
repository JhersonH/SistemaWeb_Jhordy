from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductCategory
from .forms import ProductCategoryForm
from django.contrib import messages
from distribution.decorators import role_required


@login_required
def category_list(request):
    categories = ProductCategory.objects.all()
    return render(request, "product_categories/list.html", {"categories": categories})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def category_create(request):
    form = ProductCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_categories:category_list')
    return render(request, "product_categories/form.html", {"form": form, "title": "Nueva Categoría"})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def category_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    form = ProductCategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('product_categories:category_list')
    return render(request, "product_categories/form.html", {"form": form, "title": "Editar Categoría"})


@login_required
@role_required(['ops_manager', 'warehouse_manager', 'inventory_controller'])
def category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect('product_categories:category_list')
    return render(request, "product_categories/delete_confirm.html", {"category": category})
