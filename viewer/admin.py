from django.contrib import admin
from .models import Company, Executive, RegisteredOffice, Employee, Revenue, CompanyDebt

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'year_of_foundation', 'registered_office', 'registered_office_city', 'employee_count', 'revenue_year', 'YoY_increase_in_sales')

@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('executive_name', 'executive_address', 'executive_city', 'executive_year_of_change')

@admin.register(RegisteredOffice)
class RegisteredOfficeAdmin(admin.ModelAdmin):
    list_display = ('registered_office', 'registered_office_city')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'employee_count')

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'revenue_year', 'YoY_increase_in_sales')

@admin.register(CompanyDebt)
class CompanyDebtAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'tax_office_debt', 'social_insurance_agency_debt', 'health_insurance_company_debt')
