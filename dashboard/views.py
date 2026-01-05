from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from services.models import ServiceProvider, Category
from locations.models import Village
import csv
from django.http import HttpResponse

@staff_member_required
def admin_dashboard(request):
    # 1. Basic Counters
    total_providers = ServiceProvider.objects.count()
    total_villages = Village.objects.count()
    total_categories = Category.objects.count()

    # 2. Charts Data
    # --- Category Chart ---
    cat_data = ServiceProvider.objects.values('category__name').annotate(count=Count('id')).order_by('-count')[:10] # Top 10 only
    cat_labels = [item['category__name'] for item in cat_data]
    cat_counts = [item['count'] for item in cat_data]

    # --- Village Chart ---
    vil_data = ServiceProvider.objects.values('village__name').annotate(count=Count('id')).order_by('-count')[:5]
    vil_labels = [item['village__name'] for item in vil_data]
    vil_counts = [item['count'] for item in vil_data]

    # 3. NEW: Verification Status (Safety Data)
    verified_count = ServiceProvider.objects.filter(is_verified=True).count()
    pending_count = total_providers - verified_count
    
    # 4. NEW: Recent 5 Registrations (Live Activity)
    recent_providers = ServiceProvider.objects.all().order_by('-created_at')[:5]

    context = {
        'total_providers': total_providers,
        'total_villages': total_villages,
        'total_categories': total_categories,
        'cat_labels': cat_labels,
        'cat_counts': cat_counts,
        'vil_labels': vil_labels,
        'vil_counts': vil_counts,
        # Naya Data
        'verified_count': verified_count,
        'pending_count': pending_count,
        'recent_providers': recent_providers,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


# --- Download Report Function (Ye wahi rahega) ---
@staff_member_required
def download_report(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="GramYog_Report.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Phone', 'Category', 'Village', 'District'])

        # "select_related" use kar rahe hain taaki database fast chale
        providers = ServiceProvider.objects.all().select_related('category', 'village', 'district', 'user')
        
        for p in providers:
            # Safe tarika: Agar koi cheez missing hai to "N/A" likh do, crash mat karo
            p_id = p.id
            p_name = p.full_name if p.full_name else "Unknown"
            p_phone = p.user.username if p.user else "No User"
            p_cat = p.category.name if p.category else "No Category"
            p_vil = p.village.name if p.village else "No Village"
            p_dist = p.district.name if p.district else "No District"

            writer.writerow([p_id, p_name, p_phone, p_cat, p_vil, p_dist])

        return response
        
    except Exception as e:
        # Agar fir bhi koi error aaye, to user ko simple text dikha do (Crash mat hone do)
        return HttpResponse(f"Report download failed: {str(e)}", status=500)