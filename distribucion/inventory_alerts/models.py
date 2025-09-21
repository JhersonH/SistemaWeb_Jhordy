from django.db import models
from inventory_product.models import Product
from inventory_stock.models import StockLocation

class StockAlert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE, verbose_name="Ubicación")
    minimum_quantity = models.PositiveIntegerField(verbose_name="Cantidad mínima")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'location')
        verbose_name = "Alerta de Stock Mínimo"
        verbose_name_plural = "Alertas de Stock Mínimo"

    def __str__(self):
        return f"Alerta: {self.product.name} - {self.location.name} < {self.minimum_quantity}"
