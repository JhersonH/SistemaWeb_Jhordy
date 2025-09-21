from django.db import models
from product_categories.models import ProductCategory

class Product(models.Model):
    code = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20, choices=[
        ('unit', 'Unidad'),
        ('package', 'Paquete'),
        ('box', 'Caja'),
        ('other', 'Otro'),
    ])
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    min_stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last = Product.objects.all().order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.code = f"P{next_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
