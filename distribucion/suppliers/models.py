# suppliers/models.py
from django.db import models
from django.core.validators import RegexValidator

class Supplier(models.Model):
    name = models.CharField("Nombre del proveedor", max_length=150)
    contact_name = models.CharField(
        "Persona de contacto",
        max_length=150,
        blank=True,
        null=True
    )
    phone = models.CharField(
        "Teléfono",
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\d{7,15}$', message="Ingrese solo números (7-15 dígitos).")]
    )
    email = models.EmailField("Correo electrónico", blank=True, null=True)
    address = models.TextField(default="", blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
