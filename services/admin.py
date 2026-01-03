from django.contrib import admin
from .models import Category, ServiceProvider

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # Slug apne aap ban jayega name type karte hi
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category', 'phone_number', 'district', 'village', 'is_verified')
    list_filter = ('is_verified', 'category', 'district') # Filter karne ke liye side bar
    search_fields = ('full_name', 'phone_number', 'village__name') # Search bar
    list_editable = ('is_verified',) # Admin list se hi verify tick kar sakega
    autocomplete_fields = ['village', 'district', 'state']