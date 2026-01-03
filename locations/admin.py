from django.contrib import admin
from .models import State, District, Village

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    search_fields = ['name', 'state__name'] # District + State search
    list_filter = ('state',)

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    # --- YE HAI JADU ---
    # Ab tu "Shivrajpur Katni" likhega to mil jayega
    search_fields = ['name', 'district__name', 'district__state__name'] 
    
    list_filter = ('district__state',)
    
    # List me bhi District ka naam dikha dete hain taaki confusion na ho
    list_display = ('name', 'district', 'pincode')