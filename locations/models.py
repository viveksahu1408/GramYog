from django.db import models

# 1. State (Rajya) Model
class State(models.Model):
    # Name column: Rajya ka naam (e.g., Madhya Pradesh)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # Admin panel me naam dikhega, object nahi

# 2. District (Zila) Model
class District(models.Model):
    # Foreign Key: Har Zila ek State se juda hota hai.
    # on_delete=models.CASCADE ka matlab: Agar MP delete hua, to Katni bhi delete ho jayega.
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 3. Village (Gaon) Model
class Village(models.Model):
    # Foreign Key: Har Gaon ek Zile se juda hota hai.
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='villages')
    name = models.CharField(max_length=100)
    
    # Pincode optional rakha hai abhi (blank=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.name
    

# locations/models.py

class VillageDistance(models.Model):
    # Kahan se? (Main Gaon)
    from_village = models.ForeignKey(Village, related_name='neighbors', on_delete=models.CASCADE)
    
    # Kahan tak? (Padosi Gaon)
    to_village = models.ForeignKey(Village, related_name='neighbor_of', on_delete=models.CASCADE)
    
    # Kitni door? (Km mein)
    distance_km = models.FloatField(verbose_name="Doori (KM)")

    class Meta:
        # Ek rishta do baar na ban jaye (Shivrajpur -> Badkhera ek hi baar ho)
        unique_together = ('from_village', 'to_village')
        ordering = ['distance_km'] # Jo paas hai wo pehle aayega

    def __str__(self):
        return f"{self.from_village} -> {self.to_village} ({self.distance_km} km)"    