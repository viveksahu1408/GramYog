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