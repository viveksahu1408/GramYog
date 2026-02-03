from django.contrib import admin
from .models import State, District, Village, VillageDistance # VillageDistance import karna mat bhoolna

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

@admin.register(VillageDistance)
class VillageDistanceAdmin(admin.ModelAdmin):
    list_display = ('from_village', 'to_village', 'distance_km')
    #list_filter = ('from_village',)
    # Search box lagaya taaki dropdown ghoome nahi (Lock problem fix)
    #autocomplete_fields = ['from_village', 'to_village'] 
    raw_id_fields = ('from_village', 'to_village')   

    