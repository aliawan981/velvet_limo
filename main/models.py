from django.conf import settings
from django.db import models


class ContactForm(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.phone}"

    class Meta:
        ordering = ['-created_at']


class ClientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class QuoteRequest(models.Model):
    SERVICE_ONE_WAY = 'one_way'
    SERVICE_RETURN = 'return'
    SERVICE_HOURLY = 'hourly'

    SERVICE_TYPE_CHOICES = [
        (SERVICE_ONE_WAY, 'One Way'),
        (SERVICE_RETURN, 'Return'),
        (SERVICE_HOURLY, 'Hourly'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quote_requests',
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default=SERVICE_ONE_WAY)
    pickup = models.CharField(max_length=255)
    dropoff = models.CharField(max_length=255, blank=True)
    stop = models.CharField(max_length=255, blank=True)
    trip_date = models.DateField()
    trip_time = models.TimeField()
    riders = models.PositiveIntegerField(default=1)
    return_date = models.DateField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)
    return_pickup = models.CharField(max_length=255, blank=True)
    hours = models.PositiveIntegerField(null=True, blank=True)
    hourly_area = models.CharField(max_length=255, blank=True)
    hourly_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_service_type_display()}"

    class Meta:
        ordering = ['-created_at']
