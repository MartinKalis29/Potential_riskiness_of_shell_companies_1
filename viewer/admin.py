from django.contrib import admin
from viewer.models import Company, Executive, RegisteredOffice, Employee, Revenue, CompanyDebt


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'company_id', 'company_name', 'year_of_foundation', 'executive_year_of_change', 'executive_change_count'
    )
    search_fields = ('company_name',)
    list_filter = ('year_of_foundation',)


@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('executive_name', 'executive_address', 'executive_city')
    search_fields = ('executive_name', 'executive_city')


@admin.register(RegisteredOffice)
class RegisteredOfficeAdmin(admin.ModelAdmin):
    list_display = ('company', 'registered_office_address', 'registered_office_city')
    search_fields = ('company__company_name', 'registered_office_city')
    list_filter = ('registered_office_city',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('company', 'employee_count')
    search_fields = ('company__company_name',)


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('company', 'revenue_year', 'YoY_increase_in_sales')
    search_fields = ('company__company_name', 'revenue_year')
    list_filter = ('company__company_name',)


@admin.register(CompanyDebt)
class CompanyDebtAdmin(admin.ModelAdmin):
    list_display = ('company', 'tax_office_debt', 'social_insurance_agency_debt', 'health_insurance_company_debt')
    search_fields = ('company__company_name',)
