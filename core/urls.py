from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from pages import views
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('fleet/', views.fleet, name='fleet'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog, name='blog'),
    path('contact/', main_views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
