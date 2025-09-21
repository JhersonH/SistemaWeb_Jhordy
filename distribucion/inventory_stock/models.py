# inventory_stock/models.py

from django.db import models
from inventory_product.models import Product

class StockLocation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ubicación")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.name

class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad disponible")
