from django.db import models
from locations.models import Village
from services.models import ServiceProvider
# ... baki models ke neeche ...

class Scheme(models.Model):
    title = models.CharField(max_length=200, verbose_name="Yojana Ka Naam")
    description = models.TextField(verbose_name="Choti Jankari")
    link = models.URLField(verbose_name="Website Link (Apply Karne Ke Liye)")
    icon_image = models.ImageField(upload_to='schemes/', verbose_name="Logo/Icon", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active Hai?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Notice(models.Model):
    LEVEL_CHOICES = [
        ('DISTRICT', 'Zila Star (Sabke liye)'),
        ('VILLAGE', 'Gram Star (Sirf ek gaon)'),
    ]

    title = models.CharField(max_length=200, verbose_name="Notice / Khabar")
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='DISTRICT')
    
    # Agar ye khali hai = Sabko dikhega. Agar bhara hai = Sirf us gaon ko.
    target_village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Kis Gaon ke liye?")
    
    is_active = models.BooleanField(default=True, verbose_name="Live dikhana hai?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# core/models.py

class Product(models.Model):
    # Kaun bech raha hai? (Provider link)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='products')
    
    name = models.CharField(max_length=100, verbose_name="Item ka Naam") # e.g. Aam ka Achar
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Keemat (Rs)")
    image = models.ImageField(upload_to='products/', verbose_name="Item ki Photo")
    description = models.TextField(blank=True, verbose_name="Item ki Jankari")
    
    is_available = models.BooleanField(default=True, verbose_name="Stock mein hai?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Rs.{self.price}"    