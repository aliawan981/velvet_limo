from django.contrib import admin

from .models import ClientReview, Fleet, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'short_description')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'title')


@admin.register(Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'vehicle_name', 'passengers', 'luggage', 'is_active', 'order', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'vehicle_name', 'description')
    list_editable = ('category', 'is_active', 'order')
    ordering = ('category', 'order', 'title')


@admin.register(ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_title', 'rating', 'is_active', 'order', 'created_at', 'updated_at')
    list_filter = ('is_active', 'rating', 'created_at', 'updated_at')
    search_fields = ('client_name', 'client_title', 'review')
    list_editable = ('rating', 'is_active', 'order')
    ordering = ('order', '-created_at')
