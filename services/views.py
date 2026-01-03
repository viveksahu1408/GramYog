from django.shortcuts import render, redirect
from .forms import ProviderRegistrationForm
from django.contrib.auth.models import User
from locations.models import District, Village
from django.contrib.auth import login  # <--- YE IMPORT JOD (Zaroori)
from django.contrib.auth.decorators import login_required # <--- YE BHI
from .models import ServiceProvider
from django.shortcuts import get_object_or_404 # Ye import upar jod lena
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages # Error dikhane ke liye
from django.contrib.auth import logout # <--- Ye import upar check kar lena



# 1. Registration Page dikhane wala View
def register_provider(request):
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Check karo user pehle se login hai kya?
            if request.user.is_authenticated:
                user = request.user
            else:
                # Naya User banao
                phone = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                # Check karo agar number pehle se hai
                if User.objects.filter(username=phone).exists():
                     user = User.objects.get(username=phone)
                else:
                     user = User.objects.create_user(username=phone, password=password)
                
                # Turant Login karao (Magic Line)
                login(request, user)

            # Service save karo
            provider = form.save(commit=False)
            provider.user = user
            provider.save()
            
            return redirect('profile') # Ab Home nahi, Profile par bhejo
    else:
        form = ProviderRegistrationForm()

    return render(request, 'services/register.html', {'form': form})

# --- NAYA PROFILE VIEW ---
@login_required(login_url='register_provider') # Agar login nahi hai to register page bhejo
def profile(request):
    # User ki saari services (Tractor, Chakki, etc.)
    my_services = ServiceProvider.objects.filter(user=request.user)
    
    return render(request, 'services/profile.html', {'services': my_services})



# 2. AJAX View: State -> District load karne ke liye
def load_districts(request):
    state_id = request.GET.get('state')
    districts = District.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'services/dropdown_list_options.html', {'options': districts})

# 3. AJAX View: District -> Village load karne ke liye
def load_villages(request):
    district_id = request.GET.get('district')
    villages = Village.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'services/dropdown_list_options.html', {'options': villages})


@login_required
def edit_service(request, pk):
    # Sirf wahi service edit hogi jo user ki apni hai (Security)
    service = get_object_or_404(ServiceProvider, pk=pk, user=request.user)

    if request.method == 'POST':
        # Instance=service ka matlab hai purane data ko update karo, naya mat banao
        form = ProviderRegistrationForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('profile') # Save hone ke baad Profile par wapas
    else:
        # Pehli baar mein purana data form mein bhara hua dikhao
        form = ProviderRegistrationForm(instance=service)

    return render(request, 'services/edit_service.html', {'form': form, 'service': service})


#login code 
def login_view(request):
    if request.method == 'POST':
        # Hum phone number ko hi username maan rahe hain
        phone = request.POST.get('username') 
        passw = request.POST.get('password')
        
        # Database mein check karo kya ye banda hai?
        user = authenticate(request, username=phone, password=passw)
        
        if user is not None:
            login(request, user) # Darwaza kholo
            return redirect('profile') # Seedha Profile par bhejo
        else:
            messages.error(request, "Galat Phone Number ya Password!")
    
    return render(request, 'services/login.html')

def custom_logout(request):
    logout(request) # Server se user ko hatao
    return redirect('home') # Seedha Home page par bhej do