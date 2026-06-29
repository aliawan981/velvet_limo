from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from main.models import ClientProfile, ContactForm, QuoteRequest
from pages.models import Fleet, Service

from .forms import FleetForm, ServiceForm


@staff_member_required(login_url='admin:login')
def dashboard_home(request):
    context = {
        'total_services': Service.objects.count(),
        'active_services': Service.objects.filter(is_active=True).count(),
        'total_fleet': Fleet.objects.count(),
        'active_fleet': Fleet.objects.filter(is_active=True).count(),
        'total_client_profiles': ClientProfile.objects.count(),
        'total_contact_forms': ContactForm.objects.count(),
        'total_quote_requests': QuoteRequest.objects.count(),
    }
    return render(request, 'dashboard/home.html', context)


def _delete_record(request, instance, redirect_name, success_message, object_type):
    if request.method == 'POST':
        instance.delete()
        messages.success(request, success_message)
        return redirect(redirect_name)

    return render(request, 'dashboard/confirm_delete.html', {
        'object': instance,
        'object_type': object_type,
        'cancel_url': redirect_name,
    })


@staff_member_required(login_url='admin:login')
def service_list(request):
    services = Service.objects.all().order_by('order', 'title')
    return render(request, 'dashboard/service_list.html', {'services': services})


@staff_member_required(login_url='admin:login')
def service_add(request):
    form = ServiceForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service added successfully.')
        return redirect('dashboard_services')
    return render(request, 'dashboard/service_form.html', {'form': form, 'title': 'Add Service'})


@staff_member_required(login_url='admin:login')
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=service)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Service updated successfully.')
        return redirect('dashboard_services')
    return render(request, 'dashboard/service_form.html', {'form': form, 'title': 'Edit Service', 'object': service})


@staff_member_required(login_url='admin:login')
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        return redirect('dashboard_services')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': service,
        'object_type': 'Service',
        'cancel_url': 'dashboard_services',
    })


@staff_member_required(login_url='admin:login')
def fleet_list(request):
    fleets = Fleet.objects.all().order_by('order', 'title')
    return render(request, 'dashboard/fleet_list.html', {'fleets': fleets})


@staff_member_required(login_url='admin:login')
def fleet_add(request):
    form = FleetForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Fleet vehicle added successfully.')
        return redirect('dashboard_fleet')
    return render(request, 'dashboard/fleet_form.html', {'form': form, 'title': 'Add Fleet'})


@staff_member_required(login_url='admin:login')
def fleet_edit(request, pk):
    fleet = get_object_or_404(Fleet, pk=pk)
    form = FleetForm(request.POST or None, request.FILES or None, instance=fleet)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Fleet vehicle updated successfully.')
        return redirect('dashboard_fleet')
    return render(request, 'dashboard/fleet_form.html', {'form': form, 'title': 'Edit Fleet', 'object': fleet})


@staff_member_required(login_url='admin:login')
def fleet_delete(request, pk):
    fleet = get_object_or_404(Fleet, pk=pk)
    return _delete_record(request, fleet, 'dashboard_fleet', 'Fleet vehicle deleted successfully.', 'Fleet')


@staff_member_required(login_url='admin:login')
def client_profile_list(request):
    client_profiles = ClientProfile.objects.select_related('user').order_by('-created_at')
    return render(request, 'dashboard/client_profile_list.html', {'client_profiles': client_profiles})


@staff_member_required(login_url='admin:login')
def client_profile_delete(request, pk):
    client_profile = get_object_or_404(ClientProfile, pk=pk)
    return _delete_record(
        request,
        client_profile,
        'dashboard_client_profiles',
        'Client profile deleted successfully.',
        'Client Profile',
    )


@staff_member_required(login_url='admin:login')
def contact_form_list(request):
    contact_forms = ContactForm.objects.all().order_by('-created_at')
    return render(request, 'dashboard/contact_form_list.html', {'contact_forms': contact_forms})


@staff_member_required(login_url='admin:login')
def contact_form_delete(request, pk):
    contact_form = get_object_or_404(ContactForm, pk=pk)
    return _delete_record(
        request,
        contact_form,
        'dashboard_contact_forms',
        'Contact form deleted successfully.',
        'Contact Form',
    )


@staff_member_required(login_url='admin:login')
def quote_request_list(request):
    quote_requests = QuoteRequest.objects.select_related('user').order_by('-created_at')
    return render(request, 'dashboard/quote_request_list.html', {'quote_requests': quote_requests})


@staff_member_required(login_url='admin:login')
def quote_request_delete(request, pk):
    quote_request = get_object_or_404(QuoteRequest, pk=pk)
    return _delete_record(
        request,
        quote_request,
        'dashboard_quote_requests',
        'Quote request deleted successfully.',
        'Quote Request',
    )
