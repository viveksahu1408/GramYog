from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_provider, name='register_provider'),
    
    # Ye HTMX wale URLs hain
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-villages/', views.load_villages, name='ajax_load_villages'),
    path('profile/', views.profile, name='profile'),
    path('edit-service/<int:pk>/', views.edit_service, name='edit_service'),
    path('login/', views.login_view, name='login'),


]