from django.db import models
from inventory_product.models import Product
from product_categories.models import ProductCategory
from inventory_stock.models import StockLocation
from django.contrib.auth.models import User
from transport.models import Trip
from suppliers.models import Supplier

class ProductReception(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Recibido por")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity_received = models.PositiveIntegerField(verbose_name="Cantidad Recibida")
    reception_date = models.DateField(auto_now_add=True, verbose_name="Fecha de Recepción")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Proveedor")
    location = models.ForeignKey(StockLocation, on_delete=models.CASCADE, verbose_name="Ubicación de Almacén")
    notes = models.TextField(blank=True, verbose_name="Observaciones")

    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Viaje Asociado")

    class Meta:
        verbose_name = "Recepción de Producto"
        verbose_name_plural = "Recepciones de Productos"
        ordering = ['-reception_date']

    def __str__(self):
        return f"{self.product.name} - {self.quantity_received} unidades"
