from django.contrib import admin
from .models import Company, Executive, RegisteredOffice, Employee, Revenue, CompanyDebt


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'company_name', 'year_of_foundation', 'executive_year_of_change', 'executive_change_count')


@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('executive_name', 'executive_address', 'executive_city')


@admin.register(RegisteredOffice)
class RegisteredOfficeAdmin(admin.ModelAdmin):
    list_display = ('registered_office_address', 'registered_office_city', 'company')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_count', 'company')


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('revenue_year', 'YoY_increase_in_sales', 'company')


@admin.register(CompanyDebt)
class CompanyDebtAdmin(admin.ModelAdmin):
    list_display = ('tax_office_debt', 'social_insurance_agency_debt', 'health_insurance_company_debt', 'company')
