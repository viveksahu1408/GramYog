from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path('register/', views.register_provider, name='register_provider'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'), # <--- Ye Joda (Logout ke liye)

    # Search & List URLs (Jo Error de raha tha)
    path('all/', views.service_list, name='service_list'),  # <--- YE HAI FIX (Search Button isse dhoond raha tha)
    path('category/<slug:category_slug>/', views.service_list, name='service_list_by_category'), # Filter ke liye

    # Detail URL
    path('details/<int:pk>/', views.service_detail, name='service_detail'),

    # Profile & Management
    path('profile/', views.profile, name='profile'),
    path('edit-service/<int:pk>/', views.edit_service, name='edit_service'),

    # HTMX / AJAX URLs
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('ajax/load-villages/', views.load_villages, name='ajax_load_villages'),
]