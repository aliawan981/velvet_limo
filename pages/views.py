from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def fleet(request):
    return render(request, 'fleet-list.html')

def services(request):
    return render(request, 'service-grid.html')

def blog(request):
    return render(request, 'blog-list.html')

def contact(request):
    return render(request, 'contact.html')
def privacy(request):
    return render(request, 'privacy.html')