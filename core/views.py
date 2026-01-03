from django.shortcuts import render,get_object_or_404
from services.models import Category, ServiceProvider
from django.db.models import Q  # <--- Ye line sabse upar add karna zaroori hai
from services.forms import LocationSelectForm
from locations.models import Village
from django.shortcuts import render, redirect  # <--- 'redirect' yahan add kar de
from django.db.models import Count # <--- Ye zaroori h ginti karne ke liye
from services.models import Review
from .models import Scheme
from django.http import JsonResponse
from locations.models import District, Village

def home(request):
    # Database se saari categories uthao
    categories = Category.objects.all()
    
    context = {
        'categories': categories
    }
    return render(request, 'core/home.html', context)

def service_list(request, category_slug):
    # 1. Kaunsi category click ki gayi?
    category = get_object_or_404(Category, slug=category_slug)
    
    # 2. Us category ke providers dhundo
    providers = ServiceProvider.objects.filter(category=category, is_available=True)
    
    # --- YE FILTER JODA HAI (LOCATION LOGIC) ---
    # Check karo session me koi gaon saved hai kya?
    user_village_id = request.session.get('user_village_id')
    
    if user_village_id:
        # Agar haan, to sirf usi gaon ke providers filter karo
        providers = providers.filter(village_id=user_village_id)


    context = {
        'category': category,
        'providers': providers
    }
    return render(request, 'core/service_list.html', context)    
#this is for search anything
def search(request):
    query = request.GET.get('q') # Search box me kya likha tha?
    providers = []
    
    if query:
        # Magic Query: Naam OR Category OR Village teeno me dhoondo
        providers = ServiceProvider.objects.filter(
            Q(full_name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(village__name__icontains=query) | 
            Q(district__name__icontains=query)
        ).filter(is_available=True) # Sirf jo available hain unhe dikhao
    
        # --- YE FILTER JODA HAI ---
        # Search me bhi sirf selected gaon ke log dikhao
        user_village_id = request.session.get('user_village_id')
        if user_village_id:
            providers = providers.filter(village_id=user_village_id)

    context = {
        'query': query,
        'providers': providers,
    }
    # Hum wahi list wala page reuse karenge result dikhane ke liye
    return render(request, 'core/service_list.html', context)

#Location update karne ke liye 
def change_location(request):
    if request.method == 'POST':
        form = LocationSelectForm(request.POST)
        if form.is_valid():
            # User ne jo gaon select kiya, use Session me daal do
            village_obj = form.cleaned_data['village']
            
            request.session['user_village_id'] = village_obj.id
            request.session['user_village_name'] = village_obj.name
            
            return redirect('home') # Wapas ghar bhejo
    else:
        form = LocationSelectForm()

    return render(request, 'core/change_location.html', {'form': form})

#dashboard analytics
def dashboard(request):
    # 1. Total Counts (KPIs)
    total_providers = ServiceProvider.objects.count()
    total_villages = ServiceProvider.objects.values('village').distinct().count()
    total_categories = Category.objects.count()

    # 2. Chart Data: Kis Category me kitne log hain?
    category_data = ServiceProvider.objects.values('category__name').annotate(count=Count('id')).order_by('-count')[:5]
    
    # Lists bana rahe hain taaki Javascript me use kar sakein
    cat_labels = [item['category__name'] for item in category_data]
    cat_counts = [item['count'] for item in category_data]

    # 3. Chart Data: Kis Gaon se sabse zyada log hain?
    village_data = ServiceProvider.objects.values('village__name').annotate(count=Count('id')).order_by('-count')[:5]
    
    vil_labels = [item['village__name'] for item in village_data]
    vil_counts = [item['count'] for item in village_data]

    context = {
        'total_providers': total_providers,
        'total_villages': total_villages,
        'total_categories': total_categories,
        'cat_labels': cat_labels,
        'cat_counts': cat_counts,
        'vil_labels': vil_labels,
        'vil_counts': vil_counts,
    }
    return render(request, 'core/dashboard.html', context)


#service provider ki details page
def service_detail(request, pk):
    provider = get_object_or_404(ServiceProvider, pk=pk)
    
    # Agar Form Submit hua hai (Review likha hai)
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Review Save karo
        Review.objects.create(
            provider=provider,
            user=request.user,
            rating=rating,
            comment=comment
        )
        return redirect('service_detail', pk=pk) # Page refresh karo

    # Purane reviews lekar aao
    reviews = provider.reviews.all().order_by('-created_at')
    
    context = {
        'provider': provider,
        'reviews': reviews,
    }
    return render(request, 'core/service_detail.html', context)

#schemes ke liye h ye to 
def schemes(request):
    # Sirf wahi schemes dikhao jo 'Active' hain
    schemes_list = Scheme.objects.filter(is_active=True).order_by('-created_at')
    
    return render(request, 'core/schemes.html', {'schemes': schemes_list})

def load_districts(request):
    state_id = request.GET.get('state_id')
    districts = District.objects.filter(state_id=state_id).order_by('name').values('id', 'name')
    return JsonResponse(list(districts), safe=False)

def load_villages(request):
    district_id = request.GET.get('district_id')
    villages = Village.objects.filter(district_id=district_id).order_by('name').values('id', 'name')
    return JsonResponse(list(villages), safe=False)