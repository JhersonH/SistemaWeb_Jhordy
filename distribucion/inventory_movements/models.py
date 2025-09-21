from django.db import models
from inventory_product.models import Product
from django.contrib.auth.models import User
from inventory_stock.models import StockLocation
from transport.models import Trip

class InventoryMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('input', 'Entrada'),
        ('output', 'Salida'),
        ('adjustment', 'Ajuste'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ubicación")
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Viaje asociado")
    applied = models.BooleanField(default=False)

    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"
