from locations.models import State, District, Village
from services.models import Category

print("🚀 Demo Data banana shuru...")

# 1. State Banao
mp, created = State.objects.get_or_create(name="Madhya Pradesh")
up, created = State.objects.get_or_create(name="Uttar Pradesh")


# 2. Districts Banao
katni, _ = District.objects.get_or_create(name="Katni", state=mp)
jabalpur, _ = District.objects.get_or_create(name="Jabalpur", state=mp)
bhopal, _ = District.objects.get_or_create(name="Bhopal", state=mp)

# 3. Villages Banao (Katni ke)
villages = ["Shivrajpur", "Badkhera", "Kuthla", "Madhav Nagar", "Sleemanabad"]
for v_name in villages:
    Village.objects.get_or_create(name=v_name, district=katni)

# 4. Categories Banao (Dukanein)
categories = [
    ("Tractor", "fas fa-tractor"),
    ("Electrician", "fas fa-bolt"),
    ("Plumber", "fas fa-wrench"),
    ("Raj Mistri", "fas fa-hammer"),
    ("Painter", "fas fa-paint-roller"),
    ("Labor", "fas fa-hard-hat"),
    ("Driver", "fas fa-car")
]

for name, icon in categories:
    # Icon code agar model mein nahi hai to ignore ho jayega
    Category.objects.get_or_create(name=name)

print("✅ Demo Data Successfully Ban Gaya!")