import requests
import json
from django.core.management.base import BaseCommand
from django.db import transaction
from locations.models import State, District, Village

class Command(BaseCommand):
    help = 'Loads Indian States, Districts, and Villages from JSON URL'

    def handle(self, *args, **kwargs):
        url = "https://raw.githubusercontent.com/pranshumaheshwari/indian-cities-and-villages/refs/heads/master/data.json"
        
        self.stdout.write(self.style.WARNING(f'Step 1: Downloading data...'))
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR('Failed to download file'))
                return
            
            data_list = response.json()
            self.stdout.write(self.style.SUCCESS(f'Download complete! Starting Import...'))

            with transaction.atomic():
                for state_data in data_list:
                    state_name = state_data.get('state')
                    
                    # Agar State ka naam hi gayab hai to skip karo
                    if not state_name:
                        continue

                    state_obj, created = State.objects.get_or_create(name=state_name)
                    if created:
                        print(f"Processing: {state_name}")
                    
                    districts_list = state_data.get('districts', [])
                    for dist_data in districts_list:
                        district_name = dist_data.get('district')
                        
                        if not district_name:
                            continue

                        district_obj, _ = District.objects.get_or_create(
                            name=district_name, 
                            state=state_obj
                        )
                        
                        sub_districts = dist_data.get('subDistricts', [])
                        villages_to_create = []
                        
                        for sub_dist in sub_districts:
                            village_list = sub_dist.get('villages', [])
                            
                            for v_name in village_list:
                                # --- YE HAI WO FIX (FILTER) ---
                                # Check karega ki naam None to nahi hai aur Khali string to nahi hai
                                if v_name and str(v_name).strip():
                                    villages_to_create.append(Village(
                                        name=str(v_name).strip(), # Extra space hata dega
                                        district=district_obj
                                    ))
                        
                        if villages_to_create:
                            Village.objects.bulk_create(villages_to_create, batch_size=5000)

            self.stdout.write(self.style.SUCCESS('MISSION COMPLETE! 🔥 Saara Data aa gaya.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))