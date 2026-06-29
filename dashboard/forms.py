from django import forms

from pages.models import Fleet, Service


class DashboardFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'dashboard-input')


class ServiceForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Service
        fields = ('title', 'short_description', 'image', 'icon', 'is_active', 'order')
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 4}),
        }


class FleetForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Fleet
        fields = ('title', 'vehicle_name', 'description', 'image', 'passengers', 'luggage', 'is_active', 'order')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
