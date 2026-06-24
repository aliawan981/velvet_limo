from django import forms
from .models import ContactForm


class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['full_name', 'email', 'subject', 'message']
        labels = {
            'full_name': 'Full Name',
            'email': 'Email',
            'subject': 'Subject',
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
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': ''
            }),
        }
