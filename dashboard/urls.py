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
]
