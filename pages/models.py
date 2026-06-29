from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=150)
    short_description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    icon = models.ImageField(upload_to='services/icons/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Fleet(models.Model):
    title = models.CharField(max_length=150)
    vehicle_name = models.CharField(max_length=150, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='fleet/', blank=True, null=True)
    passengers = models.PositiveIntegerField(default=1)
    luggage = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        if self.vehicle_name:
            return f'{self.title} - {self.vehicle_name}'
        return self.title
