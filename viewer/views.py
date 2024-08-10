from concurrent.futures._base import LOGGER

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.forms import CharField, IntegerField, ModelForm
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, CreateView, DeleteView

from viewer.models import Company, Revenue, CompanyDebt, Executive, RegisteredOffice, Employee

from .google_sheets import get_google_sheets_data


# Create your views here.
def companies(request):
    sheet_name = "Database_companies"
    data = get_google_sheets_data(sheet_name)

    context = {
        'companies': data
    }
    return render(request, 'database.html', context)


def home(request):
    return render(request, 'home.html', {'title': 'Welcome to SafeBusiness'})


def about_us(request):
    return render(request, 'about_us.html', {'title': 'About our website'})


def statistics(request):
    return render(request, 'statistics.html', {'title': 'Statistics'})


def company_detail(request, company_id):
    sheet_name = "Database_companies"
    data = get_google_sheets_data(sheet_name)

    try:
        company_id = int(company_id)
    except ValueError:
        raise Http404("Invalid company ID")

    company = next((company for company in data if company.get('company_id') == company_id), None)
    if not company:
        raise Http404("Company does not exist")

    risk_score = 0
    risky_addresses = ["Račianska 88 B", "Tallerova 4", "Zámocká 3", "Košická 52/A"]

    if company.get('registered_office') in risky_addresses and company.get('registered_office_city') == "Bratislava":
        risk_score += 1
    if company.get('executive_change_count', 0) > 1:
        risk_score += 1
    # if company.get('employee_count', 0) == 0 or company.get('employee_count', 0) == 1:
    if company.get('employee_count', 0) == 0 or 1:
        risk_score += 1
    if company.get('YoY_increase_in_sales', 0) > 99999:
        risk_score += 1
    if company.get('tax_office_debt', 0) > 0:
        risk_score += 1
    if company.get('social_insurance_agency_debt', 0) > 0:
        risk_score += 1
    if company.get('health_insurance_company_debt', 0) > 0:
        risk_score += 1

    return render(request, 'company_detail.html',
                  {'company': company, 'risk_score': risk_score})  # upravená cesta k šablóne


def search(request):
    if request.method == "POST":
        q = request.POST.get("search")
        database_ = Company.objects.filter(company_name__icontains=q)
        context = {'search_input': q, 'database': database_}
        return render(request, "search_results.html", context)
    return render(request, "base.html")


def statistics_view(request):
    return render(request, 'statistics.html')


def top_10_yoy_sales_view(request):
    top_10_yoy_sales = Revenue.objects.order_by('-YoY_increase_in_sales')[:10]
    return render(request, 'top_10_yoy_sales.html', {'top_10_yoy_sales': top_10_yoy_sales})


def top_10_tax_debt_view(request):
    top_10_tax_debt = CompanyDebt.objects.order_by('-tax_office_debt')[:10]
    return render(request, 'top_10_tax_debt.html', {'top_10_tax_debt': top_10_tax_debt})


def top_10_social_insurance_debt_view(request):
    top_10_social_insurance_debt = CompanyDebt.objects.order_by('-social_insurance_agency_debt')[:10]
    return render(request, 'top_10_social_insurance_debt.html',
                  {'top_10_social_insurance_debt': top_10_social_insurance_debt})


def top_10_health_insurance_debt_view(request):
    top_10_health_insurance_debt = CompanyDebt.objects.order_by('-health_insurance_company_debt')[:10]
    return render(request, 'top_10_health_insurance_debt.html',
                  {'top_10_health_insurance_debt': top_10_health_insurance_debt})


def top_10_employee_count_view(request):
    top_10_employee_count = Company.objects.annotate(total_employees=Sum('employees__employee_count')).order_by(
        '-total_employees')[:10]
    return render(request, 'top_10_employee_count.html', {'top_10_employee_count': top_10_employee_count})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_of_service(request):
    return render(request, 'terms_of_service.html')


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ExecutiveModelForm(ModelForm):
    class Meta:
        model = Executive
        fields = '__all__'

    def clean_executive_name(self):
        initial_data = super().clean()
        initial = initial_data['executive_name']
        return initial.strip()


class ExecutiveFormView(StaffRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'executive_form.html'
    form_class = ExecutiveModelForm
    success_url = reverse_lazy('executive_create')  # Názov URL patternu, nie šablóny
    permission_required = 'viewer.add_executive'

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        Executive.objects.create(
            executive_name=cleaned_data['executive_name'],
            executive_address=cleaned_data['executive_address'],
            executive_city=cleaned_data['executive_city'],
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class ExecutiveCreateView(StaffRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Executive
    template_name = 'executive_form.html'
    form_class = ExecutiveModelForm
    success_url = reverse_lazy('database')
    permission_required = 'viewer.add_executive'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class CompanyModelForm(ModelForm):
    registered_office_address = CharField(max_length=255, required=True)
    registered_office_city = CharField(max_length=255, required=True)
    employee_count = IntegerField(required=False, min_value=0)
    revenue_year = IntegerField(required=False, min_value=2023, max_value=2023)
    YoY_increase_in_sales = IntegerField(required=False, min_value=0)
    tax_office_debt = IntegerField(required=False, min_value=0)
    social_insurance_agency_debt = IntegerField(required=False, min_value=0)
    health_insurance_company_debt = IntegerField(required=False, min_value=0)

    class Meta:
        model = Company
        fields = '__all__'

    def clean_company_name(self):
        initial_data = super().clean()
        initial = initial_data['company_name']
        return initial.strip()

    def __init__(self, *args, **kwargs):
        company = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if company:
            try:
                registered_office = RegisteredOffice.objects.get(company=company)
                self.fields['registered_office_address'].initial = registered_office.registered_office_address
                self.fields['registered_office_city'].initial = registered_office.registered_office_city
            except RegisteredOffice.DoesNotExist:
                pass

            try:
                employee = Employee.objects.get(company=company)
                self.fields['employee_count'].initial = employee.employee_count
            except Employee.DoesNotExist:
                pass

            try:
                revenue = Revenue.objects.get(company=company)
                self.fields['revenue_year'].initial = revenue.revenue_year
                self.fields['YoY_increase_in_sales'].initial = revenue.YoY_increase_in_sales
            except Revenue.DoesNotExist:
                pass

            try:
                company_debt = CompanyDebt.objects.get(company=company)
                self.fields['tax_office_debt'].initial = company_debt.tax_office_debt
                self.fields['social_insurance_agency_debt'].initial = company_debt.social_insurance_agency_debt
                self.fields['health_insurance_company_debt'].initial = company_debt.health_insurance_company_debt
            except CompanyDebt.DoesNotExist:
                pass

    def save(self, commit=True):
        company = super().save(commit=False)

        if commit:
            company.save()

            RegisteredOffice.objects.update_or_create(
                company=company,
                defaults={
                    'registered_office_address': self.cleaned_data['registered_office_address'],
                    'registered_office_city': self.cleaned_data['registered_office_city'],
                }
            )

            Employee.objects.update_or_create(
                company=company,
                defaults={
                    'employee_count': self.cleaned_data['employee_count'],
                }
            )

            Revenue.objects.update_or_create(
                company=company,
                defaults={
                    'revenue_year': self.cleaned_data['revenue_year'],
                    'YoY_increase_in_sales': self.cleaned_data['YoY_increase_in_sales'],
                }
            )

            CompanyDebt.objects.update_or_create(
                company=company,
                defaults={
                    'tax_office_debt': self.cleaned_data['tax_office_debt'],
                    'social_insurance_agency_debt': self.cleaned_data['social_insurance_agency_debt'],
                    'health_insurance_company_debt': self.cleaned_data['health_insurance_company_debt'],
                }
            )

        return company


class CompanyFormView(StaffRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'company_form.html'
    form_class = CompanyModelForm
    success_url = reverse_lazy('company_create')
    permission_required = 'viewer.add_company'

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        company = Company.objects.create(
            company_name=cleaned_data['company_name'],
            year_of_foundation=cleaned_data.get('year_of_foundation'),
            executive_year_of_change=cleaned_data.get('executive_year_of_change'),
            executive_change_count=cleaned_data.get('executive_change_count')
        )

        company.executives.set(cleaned_data['executives'])

        RegisteredOffice.objects.create(
            company=company,
            registered_office_address=cleaned_data['registered_office_address'],
            registered_office_city=cleaned_data['registered_office_city']
        )

        if 'employee_count' in cleaned_data:
            Employee.objects.create(
                company=company,
                employee_count=cleaned_data['employee_count']
            )

        if 'revenue_year' in cleaned_data and 'YoY_increase_in_sales' in cleaned_data:
            Revenue.objects.create(
                company=company,
                revenue_year=cleaned_data['revenue_year'],
                YoY_increase_in_sales=cleaned_data['YoY_increase_in_sales']
            )

        if 'tax_office_debt' in cleaned_data and 'social_insurance_agency_debt' in cleaned_data and 'health_insurance_company_debt' in cleaned_data:
            CompanyDebt.objects.create(
                company=company,
                tax_office_debt=cleaned_data['tax_office_debt'],
                social_insurance_agency_debt=cleaned_data['social_insurance_agency_debt'],
                health_insurance_company_debt=cleaned_data['health_insurance_company_debt']
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class CompanyCreateView(StaffRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Company
    template_name = 'company_form.html'
    form_class = CompanyModelForm
    success_url = reverse_lazy('database')
    permission_required = 'viewer.add_company'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class CompanyUpdateView(StaffRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'company_form.html'
    model = Company
    form_class = CompanyModelForm
    success_url = reverse_lazy('database')
    permission_required = 'viewer.change_company'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Company, pk=pk)

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class CompanyDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'company_confirm_delete.html'
    model = Company
    success_url = reverse_lazy('database')
    permission_required = 'viewer.delete_company'

    def test_func(self):
        return super().test_func() and self.request.user.is_superuser
