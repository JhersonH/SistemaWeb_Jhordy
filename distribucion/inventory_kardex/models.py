from django.db import models
from inventory_product.models import Product
from inventory_stock.models import StockLocation

class KardexEntry(models.Model):
    ENTRY_TYPES = [
        ('input', 'Entrada'),
        ('output', 'Salida'),
        ('adjustment', 'Ajuste'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='kardex_entries')
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=255, blank=True, help_text="Referencia como guía, factura o motivo")
    balance = models.IntegerField(help_text="Stock acumulado después de esta entrada/salida")

    class Meta:
        ordering = ['-date']
        verbose_name = "Movimiento Kardex"
        verbose_name_plural = "Movimientos Kardex"

    def __str__(self):
        return f"{self.product.name} - {self.entry_type} ({self.quantity}) el {self.date.strftime('%d/%m/%Y')}"
