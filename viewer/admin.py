from django.contrib import admin
from .models import Company, Executive, RegisteredOffice, Employee, Revenue, CompanyDebt

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_foundation', 'registered_office', 'registered_office_city', 'employee_count', 'revenue_year', 'YoY_increase_in_sales')

@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'date_of_change')

@admin.register(RegisteredOffice)
class RegisteredOfficeAdmin(admin.ModelAdmin):
    list_display = ('address', 'city')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('company', 'count')

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('company', 'yearly_revenue', 'year')

@admin.register(CompanyDebt)
class CompanyDebtAdmin(admin.ModelAdmin):
    list_display = ('company', 'tax_office_debt', 'social_insurance_debt', 'health_insurance_debt')
