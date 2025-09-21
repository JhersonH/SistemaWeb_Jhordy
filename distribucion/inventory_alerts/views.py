from django.shortcuts import render
from inventory_stock.models import ProductStock

def alert_list(request):
    alerts = ProductStock.objects.filter(
        product__is_active=True,
        product__min_stock__isnull=False
    ).select_related('product', 'location')

    alerts = [stock for stock in alerts if stock.quantity < stock.product.min_stock]

    return render(request, 'inventory_alerts/list.html', {'alerts': alerts})
