from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [
        ('ops_manager', 'Jefe de Operaciones'),
        ('warehouse_manager', 'Jefe de Almacén'),
        ('warehouse_staff', 'Operario de Almacén'),
        ('inventory_controller', 'Control de Inventario'),
        ('dispatcher', 'Despachador'),
        ('driver', 'Conductor'),
        ('viewer', 'Consulta / Solo Lectura'),
    ]

    role_type = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        unique=True,
        verbose_name='Rol'
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_role_type_display()
