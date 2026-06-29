from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('services/', views.service_list, name='dashboard_services'),
    path('services/add/', views.service_add, name='dashboard_service_add'),
    path('services/edit/<int:pk>/', views.service_edit, name='dashboard_service_edit'),
    path('services/delete/<int:pk>/', views.service_delete, name='dashboard_service_delete'),
    path('fleet/', views.fleet_list, name='dashboard_fleet'),
    path('fleet/add/', views.fleet_add, name='dashboard_fleet_add'),
    path('fleet/edit/<int:pk>/', views.fleet_edit, name='dashboard_fleet_edit'),
    path('fleet/delete/<int:pk>/', views.fleet_delete, name='dashboard_fleet_delete'),
    path('main/client-profiles/', views.client_profile_list, name='dashboard_client_profiles'),
    path('main/client-profiles/delete/<int:pk>/', views.client_profile_delete, name='dashboard_client_profile_delete'),
    path('main/contact-forms/', views.contact_form_list, name='dashboard_contact_forms'),
    path('main/contact-forms/delete/<int:pk>/', views.contact_form_delete, name='dashboard_contact_form_delete'),
    path('main/quote-requests/', views.quote_request_list, name='dashboard_quote_requests'),
    path('main/quote-requests/delete/<int:pk>/', views.quote_request_delete, name='dashboard_quote_request_delete'),
]
