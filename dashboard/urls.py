from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Link
    path('admin-dashboard/', views.admin_dashboard, name='dashboard'),
    
    # Download Link
    path('download-report/', views.download_report, name='download_report'),
]