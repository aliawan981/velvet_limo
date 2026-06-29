from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from pages.models import Fleet, Service

from .forms import FleetForm, ServiceForm


@staff_member_required(login_url='admin:login')
def dashboard_home(request):
    context = {
        'total_services': Service.objects.count(),
        'active_services': Service.objects.filter(is_active=True).count(),
        'total_fleet': Fleet.objects.count(),
        'active_fleet': Fleet.objects.filter(is_active=True).count(),
    }
    return render(request, 'dashboard/home.html', context)


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
    if request.method == 'POST':
        fleet.delete()
        messages.success(request, 'Fleet vehicle deleted successfully.')
        return redirect('dashboard_fleet')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': fleet,
        'object_type': 'Fleet',
        'cancel_url': 'dashboard_fleet',
    })
