# inventory_kardex/views.py
from django.shortcuts import render
from .models import KardexEntry
from django.http import JsonResponse
from .forms import KardexFilterForm

def kardex_list(request):
    form = KardexFilterForm(request.GET or None)
    entries = KardexEntry.objects.select_related('product', 'location').order_by('-date')

    if form.is_valid():
        product = form.cleaned_data.get('product')
        if product:
            entries = entries.filter(product=product)

    context = {
        'form': form,
        'entries': entries
    }
    return render(request, 'inventory_kardex/list.html', context)

def kardex_entries_api(request, product_id):
    entries = KardexEntry.objects.filter(product_id=product_id).select_related("product", "location").order_by("-date")

    data = [
        {
            "date": entry.date.strftime("%d/%m/%Y %H:%M"),
            "product": entry.product.name,
            "location": entry.location.name if entry.location else "-",
            "entry_type": entry.get_entry_type_display(),
            "quantity": entry.quantity,
            "balance": entry.balance,
            "reference": entry.reference or "-"
        }
        for entry in entries
    ]
    return JsonResponse({"entries": data})
