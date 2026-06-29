from django.contrib import admin

from .models import ClientProfile, ContactForm, QuoteRequest

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'user', 'created_at')
    search_fields = ('full_name', 'phone', 'user__username', 'user__email')
    readonly_fields = ('created_at',)


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'service_type', 'pickup', 'dropoff', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'pickup', 'dropoff')
    readonly_fields = ('created_at',)
