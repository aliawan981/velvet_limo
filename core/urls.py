from django.contrib import admin
from django.urls import path
from pages import views
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('fleet/', views.fleet, name='fleet'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('contact/', main_views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),

]