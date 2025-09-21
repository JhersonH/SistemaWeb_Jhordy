# product_categories/models.py

from django.db import models

class ProductCategory(models.Model):
    name = models.CharField("Nombre", max_length=100, unique=True)
    description = models.TextField("Descripción", blank=True)

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
        ordering = ["name"]

    def __str__(self):
        return self.name
