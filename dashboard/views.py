from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from services.models import ServiceProvider, Category
from locations.models import Village
import csv
from django.http import HttpResponse

@staff_member_required
def admin_dashboard(request):
    # 1. Top Cards Data (Counters)
    total_providers = ServiceProvider.objects.count()
    total_villages = Village.objects.count()
    total_categories = Category.objects.count()

    # 2. Category Chart Data (Bar Chart)
    # Database se nikalenge ki kis category mein kitne log hain
    cat_data = ServiceProvider.objects.values('category__name').annotate(count=Count('id')).order_by('-count')
    
    # Python Lists banayenge jo JavaScript mein jayenge
    cat_labels = [item['category__name'] for item in cat_data]
    cat_counts = [item['count'] for item in cat_data]

    # 3. Village Chart Data (Doughnut Chart)
    # Top 5 villages jahan sabse zyada log jude hain
    vil_data = ServiceProvider.objects.values('village__name').annotate(count=Count('id')).order_by('-count')[:5]
    
    vil_labels = [item['village__name'] for item in vil_data]
    vil_counts = [item['count'] for item in vil_data]

    context = {
        'total_providers': total_providers,
        'total_villages': total_villages,
        'total_categories': total_categories,
        'cat_labels': cat_labels,
        'cat_counts': cat_counts,
        'vil_labels': vil_labels,
        'vil_counts': vil_counts,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

# --- Download Report Function (Ye wahi rahega) ---
@staff_member_required
def download_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="GramYog_Report.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Phone', 'Category', 'Village', 'District'])

    providers = ServiceProvider.objects.all().select_related('category', 'village', 'district', 'user')
    for p in providers:
        writer.writerow([p.id, p.full_name, p.user.username, p.category.name, p.village.name, p.district.name])

    return response