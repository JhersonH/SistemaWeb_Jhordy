from django.contrib import admin
from .models import Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_type', 'created_at')
    list_filter = ('role_type',)
    search_fields = ('role_type',)
    ordering = ('role_type',)
