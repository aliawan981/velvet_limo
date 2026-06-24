from django.contrib import admin
from .models import ContactForm

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
