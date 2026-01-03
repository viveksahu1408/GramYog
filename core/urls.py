from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Ye import upar
from services import views as service_views # <--- Ye import zaroori hai

urlpatterns = [
    path('', views.home, name='home'),
    path('services/<slug:category_slug>/', views.service_list, name='service_list'),
    path('search/', views.search, name='search'),
    path('change-location/', views.change_location, name='change_location'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('provider-detail/<int:pk>/', views.service_detail, name='service_detail'),
    #ye govt ki schemes show karane ke liya
    path('schemes/', views.schemes, name='schemes'),
    path('logout/', service_views.custom_logout, name='logout'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-villages/', views.load_villages, name='ajax_load_villages'),



]