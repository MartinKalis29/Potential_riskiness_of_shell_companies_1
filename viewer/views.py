from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404

from viewer.models import Company

from .google_sheets import get_google_sheets_data


# Create your views here.
def companies(request):
    # Zadá sa názov alebo URL Google Sheets
    sheet_name = "Database_companies"
    data = get_google_sheets_data(sheet_name)

    # Spracovanie dát a ich odoslanie do šablóny alebo ako odpoveď
    context = {
        'companies': data
    }
    return render(request, 'database.html', context)  # upravená cesta k šablóne


def home(request):
    return render(request, 'home.html', {'title': 'Welcome to SafeBusiness'})


def about_us(request):
    return render(request, 'about_us.html', {'title': 'About our website'})


def statistics(request):
    return render(request, 'statistics.html', {'title': 'Statistics'})


def company_detail(request, company_id):
    sheet_name = "Database_companies"
    data = get_google_sheets_data(sheet_name)

    # Vyhľadanie konkrétnej firmy
    try:
        company_id = int(company_id)
    except ValueError:
        raise Http404("Invalid company ID")

    company = next((company for company in data if company.get('company_id') == company_id), None)
    if not company:
        raise Http404("Company does not exist")

    # Výpočet rizikového skóre
    risk_score = 0
    risky_addresses = ["Račianska 88 B", "Tallerova 4", "Zámocká 3", "Košická 52/A"]

    if company.get('registered_office') in risky_addresses and company.get('registered_office_city') == "Bratislava":
        risk_score += 1
    if company.get('executive_change_count', 0) > 1:
        risk_score += 1
    if company.get('employee_count', 0) == 0 or company.get('employee_count', 0) == 1:
        risk_score += 1
    if company.get('YoY_increase_in_sales', 0) > 99999:
        risk_score += 1
    if company.get('tax_office_debt', 0) > 0:
        risk_score += 1
    if company.get('social_insurance_agency_debt', 0) > 0:
        risk_score += 1
    if company.get('health_insurance_company_debt', 0) > 0:
        risk_score += 1

    return render(request, 'company_detail.html', {'company': company, 'risk_score': risk_score})  # upravená cesta k šablóne


def search(request):
    if request.method == "POST":
        q = request.POST.get("search")
        database_ = Company.objects.filter(company_name__icontains=q)
        context = {'search_input': q, 'database': database_}
        return render(request, "search_results.html", context)
    return render(request, "home.html")