from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from threading import Thread

from .forms import ClientLoginForm, ClientRegistrationForm, ContactFormForm, QuoteRequestForm
from .models import ClientProfile, QuoteRequest
from .microsoft_graph_mail import send_graph_mail

ADMIN_EMAIL = getattr(settings, 'ADMIN_EMAIL', '')


def _send_async_email(email_function, *args, **kwargs):
    Thread(target=email_function, args=args, kwargs=kwargs, daemon=True).start()


def _send_graph_email(subject, body, recipients):
    if not recipients:
        return

    send_graph_mail(
        subject=subject,
        body=body,
        recipients=recipients,
        sender=settings.DEFAULT_FROM_EMAIL,
    )


def _send_quote_emails(quote_request):
    admin_subject = f"New quote request from {quote_request.full_name}"
    admin_body = f"""
    New quote request received.
    
    Customer: {quote_request.full_name}
    Email: {quote_request.email}
    Phone: {quote_request.phone}
    Service type: {quote_request.get_service_type_display()}
    Pickup: {quote_request.pickup}
    Drop off: {quote_request.dropoff or '-'}
    Stop: {quote_request.stop or '-'}
    Trip date: {quote_request.trip_date}
    Trip time: {quote_request.trip_time}
    Riders: {quote_request.riders}
    Return date: {quote_request.return_date or '-'}
    Return time: {quote_request.return_time or '-'}
    Return pickup: {quote_request.return_pickup or '-'}
    Hours: {quote_request.hours or '-'}
    Hourly area: {quote_request.hourly_area or '-'}
    Hourly notes: {quote_request.hourly_notes or '-'}
    Submitted at: {quote_request.created_at}
    """.strip()

    customer_subject = 'We received your quote request'
    customer_body = f"""
    Hello {quote_request.full_name},
    
    We received your quote request and will review the details shortly.
    
    Pickup: {quote_request.pickup}
    Drop off: {quote_request.dropoff or '-'}
    Trip date: {quote_request.trip_date}
    Trip time: {quote_request.trip_time}
    
    Thank you,
    Velvet Limousine Team
    """.strip()

    _send_graph_email(admin_subject, admin_body, [ADMIN_EMAIL])
    _send_graph_email(customer_subject, customer_body, [quote_request.email])


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Your account has been created.')
            return redirect('home')
    else:
        form = ClientRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ClientLoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, 'You are now signed in.')
            next_page = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_page)
    else:
        form = ClientLoginForm(request)

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been signed out.')
    return redirect('home')


def contact(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            # Save form to database
            contact_instance = form.save()

            # Prepare email
            subject = f"New Contact Form Submission from {contact_instance.full_name}"
            message_body = f"""
            New contact form submission received:
            
            Name: {contact_instance.full_name}
            Email: {contact_instance.email}
            Phone: {contact_instance.phone}
            
            Message:
            {contact_instance.message}
            
            ---
            Submitted at: {contact_instance.created_at}
            """
            admin_email = getattr(settings, 'ADMIN_EMAIL', '')
            try:
                # Send email to admin
                _send_async_email(
                    _send_graph_email,
                    subject,
                    message_body,
                    [admin_email],
                )

                # Send confirmation email to user
                user_message = f"""
                Thank you for contacting Velvet Limousine!
                
                We have received your message and will get back to you soon.
                
                Best regards,
                Velvet Limousine Team
                """
                _send_async_email(
                    _send_graph_email,
                    'Thank you for your inquiry - Velvet Limousine',
                    user_message,
                    [contact_instance.email],
                )

                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
                return redirect('contact')
            except Exception as e:
                # Silently handle errors - still show success
                messages.success(request, 'Your message has been received! We will get back to you soon.')
                return redirect('contact')
    else:
        form = ContactFormForm()

    return render(request, 'contact.html', {'form': form})


@login_required(login_url='/login/')
def quote_request(request):
    if request.method != 'POST':
        return redirect('home')

    form = QuoteRequestForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Please complete the quote form and try again.')
        return redirect('home')

    profile = getattr(request.user, 'profile', None)
    quote_request = form.save(commit=False)
    quote_request.user = request.user
    quote_request.full_name = profile.full_name if profile else request.user.get_full_name() or request.user.username
    quote_request.email = request.user.email
    quote_request.phone = profile.phone if profile else ''
    quote_request.save()

    _send_async_email(_send_quote_emails, quote_request)
    messages.success(request, 'Your quote request was saved and submitted successfully.')

    return redirect('home')
