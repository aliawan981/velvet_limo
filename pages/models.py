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
    CATEGORY_SEDAN = 'sedan'
    CATEGORY_SUV = 'suv'
    CATEGORY_CHOICES = (
        (CATEGORY_SEDAN, 'Premium Sedan'),
        (CATEGORY_SUV, 'Premium SUV'),
    )

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_SEDAN)
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

    @property
    def description_points(self):
        return [
            line.strip().lstrip('-•*').strip()
            for line in self.description.splitlines()
            if line.strip()
        ]
