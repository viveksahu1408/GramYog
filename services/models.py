from django.db import models
from django.contrib.auth.models import User
# Hamare location wale models import kar rahe hain
from locations.models import State, District, Village

# 1. Category Model (Jaise: Electrician, Tractor, Doctor)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kaam ka Naam")
    # Icon upload karne ke liye (Images 'media/categories/' folder me jayengi)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True) # URL ke liye (e.g., gramyog.com/tractor)

    def save(self, *args, **kwargs):
        # Agar slug nahi hai to naam se bana do (Auto-generate)
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# 2. Service Provider Model (Mistri/Dukandar ki Profile)
class ServiceProvider(models.Model):
    # User se link (Login ke liye)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    
    # Personal Details
    full_name = models.CharField(max_length=200, verbose_name="Pura Naam")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Mobile Number")
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Kaam (Category)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='providers')
    description = models.TextField(blank=True, verbose_name="Apne kaam ke bare me batayein")
    experience_years = models.IntegerField(default=0, verbose_name="Kitne saal ka anubhav hai?")
    
    # Location (Dropdown wala logic)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True)
    
    # Verification & Status
    is_verified = models.BooleanField(default=False) # Blue Tick ke liye
    is_available = models.BooleanField(default=True) # Online/Offline switch
    
    # Stats (Analytics ke liye hidden fields)
    views_count = models.IntegerField(default=0) # Kitne logon ne dekha
    call_clicks = models.IntegerField(default=0) # Kitne logon ne call kiya
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.category})"
    
#rating review ke liye 
class Review(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Kisne review diya
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)]) # 1 se 5 star
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.provider.full_name}"    