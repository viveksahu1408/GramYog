from django.contrib import admin
from django.urls import path, include
from django.conf import settings          # <-- Ye photo ke liye zaroori hai
from django.conf.urls.static import static # <-- Ye bhi photo ke liye

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- CHANGE IS HERE (Is line ko Upar rakho) ---
    # Pehle check karo ki kya ye services app ka URL hai (jaise register)?
    path('services/', include('services.urls')), 
    
    # Phir baki cheezen check karo (jaise Tractor category)
    path('', include('core.urls')),

    path('dashboard/', include('dashboard.urls')),
]

# Photo dikhane ke liye ye code bhi jod dena agar nahi joda to:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)