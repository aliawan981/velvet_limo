from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import ClientProfile, ContactForm, QuoteRequest


User = get_user_model()


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


class ClientRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data['full_name'].strip()
        email = self.cleaned_data['email'].strip().lower()
        user.username = email
        user.email = email
        user.first_name = full_name
        if commit:
            user.save()
            ClientProfile.objects.update_or_create(
                user=user,
                defaults={
                    'full_name': full_name,
                    'phone': self.cleaned_data['phone'].strip(),
                },
            )
        return user


class ClientLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class QuoteRequestForm(forms.ModelForm):
    trip_date = forms.DateField(
        input_formats=['%a, %b %d, %Y', '%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'search-input datepicker', 'type': 'text'}),
    )
    return_date = forms.DateField(
        required=False,
        input_formats=['%a, %b %d, %Y', '%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'search-input datepicker', 'type': 'text'}),
    )
    trip_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'search-input', 'type': 'time'}),
    )

    class Meta:
        model = QuoteRequest
        fields = [
            'service_type',
            'pickup',
            'dropoff',
            'stop',
            'trip_date',
            'trip_time',
            'riders',
            'return_date',
            'return_time',
            'return_pickup',
            'hours',
            'hourly_area',
            'hourly_notes',
        ]
        widgets = {
            'service_type': forms.HiddenInput(),
            'pickup': forms.TextInput(attrs={'class': 'search-input'}),
            'dropoff': forms.TextInput(attrs={'class': 'search-input'}),
            'stop': forms.TextInput(attrs={'class': 'search-input'}),
            'riders': forms.NumberInput(attrs={'class': 'search-input', 'min': 1}),
            'return_time': forms.TimeInput(attrs={'class': 'search-input', 'type': 'time'}),
            'return_pickup': forms.TextInput(attrs={'class': 'search-input'}),
            'hours': forms.NumberInput(attrs={'class': 'search-input', 'min': 1}),
            'hourly_area': forms.TextInput(attrs={'class': 'search-input'}),
            'hourly_notes': forms.TextInput(attrs={'class': 'search-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        service_type = cleaned_data.get('service_type')

        if service_type == QuoteRequest.SERVICE_ONE_WAY:
            if not cleaned_data.get('pickup'):
                self.add_error('pickup', 'Pickup is required for a one-way quote.')
            if not cleaned_data.get('dropoff'):
                self.add_error('dropoff', 'Drop off is required for a one-way quote.')
        elif service_type == QuoteRequest.SERVICE_RETURN:
            required_fields = ['pickup', 'dropoff', 'return_date', 'return_time']
            for field_name in required_fields:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, 'This field is required for a return quote.')
        elif service_type == QuoteRequest.SERVICE_HOURLY:
            required_fields = ['pickup', 'hours', 'hourly_area']
            for field_name in required_fields:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, 'This field is required for an hourly quote.')

        return cleaned_data
