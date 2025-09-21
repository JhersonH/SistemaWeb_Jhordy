from django.db import models
from django.contrib.auth.models import User
from inventory_product.models import Product
from inventory_stock.models import StockLocation

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('maintenance', 'Mantenimiento'),
        ('retired', 'Baja'),
    ]
    plate = models.CharField('Placa', max_length=15, unique=True)
    brand = models.CharField('Marca', max_length=30, blank=True)
    model = models.CharField('Modelo', max_length=30, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    capacity_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume_m3 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    odometer_km = models.PositiveIntegerField(default=0)
    insurance_expiry = models.DateField('Vence SOAT/Seguro', null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.plate} ({self.get_status_display()})'

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField('Licencia', max_length=30)
    license_category = models.CharField(max_length=10, blank=True)
    license_expiry = models.DateField('Vence Licencia', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Route(models.Model):
    name = models.CharField(max_length=60)
    origin = models.ForeignKey(StockLocation, on_delete=models.CASCADE, related_name='routes_origin')
    destination = models.ForeignKey(StockLocation, on_delete=models.CASCADE, related_name='routes_destination')
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    eta_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Trip(models.Model):
    STATUS = [
        ('planned', 'Planificado'),
        ('dispatched', 'Despachado'),
        ('in_progress', 'En curso'),
        ('completed', 'Completado'),
        ('canceled', 'Cancelado'),
    ]
    code = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=STATUS, default='planned')
    odometer_start = models.PositiveIntegerField(null=True, blank=True)
    odometer_end = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    is_reception = models.BooleanField(default=False, verbose_name="Es recepción")

    def __str__(self):
        return f'{self.code} - {self.get_status_display()}'

class TripProduct(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Viaje"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    quantity = models.PositiveIntegerField("Cantidad")

    class Meta:
        verbose_name = "Producto del Viaje"
        verbose_name_plural = "Productos del Viaje"

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - {self.trip.code}"

class Stop(models.Model):
    STATUS = [
        ('pending', 'Pendiente'),
        ('delivered', 'Entregado'),
        ('failed', 'Fallido'),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    seq = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=120)
    address = models.CharField(max_length=200)
    planned_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivered_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    pod_photo = models.ImageField(upload_to='pod/', null=True, blank=True)
    signature_name = models.CharField(max_length=60, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['seq']

class Expense(models.Model):
    TYPES = [
        ('fuel', 'Combustible'),
        ('toll', 'Peaje'),
        ('parking', 'Parqueo'),
        ('other', 'Otro'),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='expenses')
    type = models.CharField(max_length=10, choices=TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.trip}'

class Incident(models.Model):
    TYPES = [
        ('breakdown', 'Avería'),
        ('accident', 'Accidente'),
        ('delay', 'Demora'),
        ('theft', 'Robo'),
        ('other', 'Otro'),
    ]

    SEVERITY_LEVELS = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='incidents')
    type = models.CharField(max_length=12, choices=TYPES)
    severity = models.PositiveSmallIntegerField(choices=SEVERITY_LEVELS, default=1)
    description = models.TextField()
    occurred_at = models.DateTimeField()
    attachment = models.FileField(upload_to='incidents/', null=True, blank=True)

    def __str__(self):
        return f'{self.trip}'