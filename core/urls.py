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
    path('quote-request/', main_views.quote_request, name='quote_request'),
    path('login/', main_views.login_view, name='login'),
    path('login.html', main_views.login_view, name='login_html'),
    path('register/', main_views.register, name='register'),
    path('register.html', main_views.register, name='register_html'),
    path('logout/', main_views.logout_view, name='logout'),
    path('logout.html', main_views.logout_view, name='logout_html'),
    path('contact.html', main_views.contact, name='contact_html'),
    path('privacy/', views.privacy, name='privacy'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
