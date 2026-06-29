from django.shortcuts import render

from .models import Fleet, Service


def home(request):
    services = Service.objects.filter(is_active=True).order_by('order')
    fleets = Fleet.objects.all().order_by('order', 'title')
    return render(request, 'index.html', {'services': services, 'fleets': fleets})

def about(request):
    return render(request, 'about.html')

def fleet(request):
    fleets = Fleet.objects.all().order_by('order', 'title')
    return render(request, 'fleet-list.html', {'fleets': fleets})

def services(request):
    services = Service.objects.filter(is_active=True).order_by('order')
    return render(request, 'service-grid.html', {'services': services})

def blog(request):
    return render(request, 'blog-list.html')

def contact(request):
    return render(request, 'contact.html')
def privacy(request):
    return render(request, 'privacy.html')
