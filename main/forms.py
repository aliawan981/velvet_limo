from django import forms
from .models import ContactForm


class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['full_name', 'email', 'phone', 'message']
        labels = {
            'full_name': 'Your Name',
            'email': 'Your Email',
            'phone': 'Your Phone',
            'message': 'Message',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': ''
            }),
        }
