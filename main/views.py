from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactFormForm


def contact(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            # Save form to database
            contact_instance = form.save()

            # Prepare email
            subject = f"New Contact Form Submission: {contact_instance.subject}"
            message_body = f"""
            New contact form submission received:
            
            Name: {contact_instance.full_name}
            Email: {contact_instance.email}
            Subject: {contact_instance.subject}
            
            Message:
            {contact_instance.message}
            
            ---
            Submitted at: {contact_instance.created_at}
            """

            try:
                # Send email to admin
                send_mail(
                    subject,
                    message_body,
                    settings.DEFAULT_FROM_EMAIL,
                    ['mahbub@velvetlimousine.com'],
                    fail_silently=True,
                )

                # Send confirmation email to user
                user_message = f"""
                Thank you for contacting Velvet Limousine!
                
                We have received your message and will get back to you soon.
                
                Best regards,
                Velvet Limousine Team
                """
                send_mail(
                    'Thank you for your inquiry - Velvet Limousine',
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_instance.email],
                    fail_silently=True,
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
