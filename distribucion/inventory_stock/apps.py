from django.apps import AppConfig


class InventoryStockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory_stock'

    def ready(self):
        import inventory_stock.signals