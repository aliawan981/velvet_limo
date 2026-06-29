from django.contrib import admin

from .models import Fleet, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'short_description')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'title')


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ('title', 'vehicle_name', 'passengers', 'luggage', 'is_active', 'order', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'vehicle_name', 'description')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'title')
