from django.db import models
from inventory_product.models import Product
from inventory_stock.models import StockLocation

class InventoryAdjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('increase', 'Incremento'),
        ('decrease', 'Disminución'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE)
    quantity = models.IntegerField("Cantidad ajustada")
    adjustment_type = models.CharField(max_length=10, choices=ADJUSTMENT_TYPES)
    reason = models.TextField("Motivo del ajuste")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Ajuste de Inventario"
        verbose_name_plural = "Ajustes de Inventario"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} ({self.adjustment_type} {self.quantity}) - {self.created_at.strftime('%Y-%m-%d')}"
