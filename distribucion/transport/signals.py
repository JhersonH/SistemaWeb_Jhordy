from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Trip
from inventory_movements.models import InventoryMovement

@receiver(post_save, sender=Trip)
def handle_trip_state_change(sender, instance, created, **kwargs):
    status = instance.status.lower()

    print(f"\n🔔 Signal activado para Trip {instance.id} - Estado: {status} - is_reception={instance.is_reception} - created={created}")

    if created:
        print("⚠️ Es una creación de Trip. Ignorado.")
        return

    elif status == "canceled":
        print("🚫 Viaje cancelado. Revirtiendo movimientos.")
        updated = InventoryMovement.objects.filter(trip=instance).update(applied=False)
        print(f"ℹ️ {updated} movimientos marcados como no aplicados.")
