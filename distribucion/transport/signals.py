from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Trip
from inventory_movements.models import InventoryMovement
from inventory_receiving.models import ProductReception
from django.db import IntegrityError
from core.middleware.thread_local import get_current_request

@receiver(post_save, sender=Trip)
def handle_trip_state_change(sender, instance, created, **kwargs):
    status = instance.status.lower()
    trip_code = instance.code
    request = get_current_request()
    user = request.user if request and request.user.is_authenticated else None

    print(f"\n🔔 Signal activado para Trip {instance.id} - Estado: {status} - is_reception={instance.is_reception} - created={created}")

    if created:
        print("⚠️ Es una creación de Trip. Ignorado.")
        return

    if status == "dispatched":
        print("📦 Generando salidas...")
        for tp in instance.products.all():
            try:
                inv = InventoryMovement.objects.create(
                    product=tp.product,
                    quantity=tp.quantity,
                    movement_type="output",
                    location=instance.route.origin,
                    description=f"Salida por viaje {trip_code}",
                    trip=instance
                )
                print(f"✅ Salida registrada: {inv.product.name} x{inv.quantity} | ID: {inv.id}")
            except IntegrityError as e:
                print(f"❌ ERROR guardando movimiento de salida: {e}")

    elif status == "completed" and instance.is_reception:
        print("📥 Generando recepciones e ingresos...")
        for tp in instance.products.all():
            try:
                rec = ProductReception.objects.create(
                    product=tp.product,
                    quantity_received=tp.quantity,
                    supplier="Proveedor X",
                    location=instance.route.destination,
                    notes=f"Recepción por viaje {trip_code}",
                    receiver = user
                )
                print(f"✅ Recepción registrada: {rec.product.name} x{rec.quantity_received} | ID: {rec.id}")
            except IntegrityError as e:
                print(f"❌ ERROR guardando recepción o ingreso: {e}")
            except Exception as e:
                print(f"❌ Error inesperado: {e}")

    elif status == "canceled":
        print("🚫 Viaje cancelado. Revirtiendo movimientos.")
        updated = InventoryMovement.objects.filter(trip=instance).update(applied=False)
        print(f"ℹ️ {updated} movimientos marcados como no aplicados.")
