from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from inventory_movements.models import InventoryMovement
from inventory_adjustments.models import InventoryAdjustment
from inventory_receiving.models import ProductReception
from inventory_stock.models import ProductStock
from inventory_kardex.models import KardexEntry


# ✅ 1. Cuando se registra un movimiento
@receiver(post_save, sender=InventoryMovement)
def update_stock_from_movement(sender, instance, created, **kwargs):
    if not created:
        return

    # Evitar duplicar Kardex si el movimiento viene de una recepción
    if hasattr(instance, "origin") and instance.origin == "reception":
        return

    product = instance.product
    location = instance.location
    qty = instance.quantity

    stock, _ = ProductStock.objects.get_or_create(product=product, location=location)

    if instance.movement_type == "input":
        stock.quantity += qty
        entry_type = "input"
    elif instance.movement_type == "output":
        if stock.quantity < qty:
            raise ValueError("Stock insuficiente para realizar esta salida.")
        stock.quantity -= qty
        entry_type = "output"
    else:
        stock.quantity += qty
        entry_type = "adjustment"

    stock.save()

    KardexEntry.objects.create(
        product=product,
        location=location,
        entry_type=entry_type,
        quantity=qty,
        reference=f"Movimiento #{instance.id}",
        balance=stock.quantity
    )


# ✅ 2. Cuando se registra un ajuste
@receiver(post_save, sender=InventoryAdjustment)
def update_stock_from_adjustment(sender, instance, created, **kwargs):
    product = instance.product
    location = instance.location
    qty = instance.quantity

    stock, _ = ProductStock.objects.get_or_create(product=product, location=location)

    # Si es edición, eliminar el registro viejo del Kardex y recalcular
    if not created:
        KardexEntry.objects.filter(reference=f"Ajuste #{instance.id}").delete()

    # Aplicar el ajuste
    if instance.adjustment_type == "increase":
        stock.quantity += qty
        entry_type = "adjustment"
    else:  # decrease
        stock.quantity -= qty
        entry_type = "adjustment"

    stock.save()

    KardexEntry.objects.create(
        product=product,
        location=location,
        entry_type=entry_type,
        quantity=qty,
        reference=f"Ajuste #{instance.id}: {instance.reason}",
        balance=stock.quantity
    )

# ✅ 3. Cuando se registra una recepción
@receiver(post_save, sender=ProductReception)
def update_stock_from_reception(sender, instance, created, **kwargs):
    if not created:
        return

    product = instance.product
    location = instance.location
    qty = instance.quantity_received

    stock, _ = ProductStock.objects.get_or_create(product=product, location=location)
    stock.quantity += qty
    stock.save()

    KardexEntry.objects.create(
        product=product,
        location=location,
        entry_type="input",
        quantity=qty,
        reference=f"Recepción de {instance.supplier}",
        balance=stock.quantity
    )
