from django.contrib import admin
from .models import Vehicle, Driver, Route, Trip, Stop, Expense, Incident

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("plate", "status", "capacity_kg", "next_maintenance")
    list_filter = ("status",)
    search_fields = ("plate",)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("user", "license_number", "license_expiry", "active")
    search_fields = ("user__username", "user__first_name", "user__last_name", "license_number")

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("name", "origin", "destination", "distance_km", "eta_minutes")
    search_fields = ("name", "origin", "destination")

class StopInline(admin.TabularInline):
    model = Stop
    extra = 0

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("code", "date", "route", "vehicle", "driver", "status")
    list_filter = ("status", "date")
    search_fields = ("code",)
    inlines = [StopInline]

admin.site.register(Expense)
admin.site.register(Incident)
