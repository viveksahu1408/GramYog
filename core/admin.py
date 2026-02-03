from django.contrib import admin

from .models import Scheme,Notice,Product# <--- Scheme import karna mat bhoolna

@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'target_village', 'is_active', 'created_at')
    list_filter = ('level', 'is_active')
    search_fields = ('title',)
    
    # --- YE HAI JADUI LINE (MAGIC FIX) ---
    # Isse dropdown hat jayega aur search ka option aayega
    # Jisse page heavy nahi hoga aur turant khulega
    raw_id_fields = ('target_village',)

#mahila SHGs ke liye 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'provider', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name', 'provider__business_name')    