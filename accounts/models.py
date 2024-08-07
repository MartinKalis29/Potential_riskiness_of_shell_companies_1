from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    employee_id_number = models.CharField(max_length=50, null=True, blank=True)
    personal_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    employee_count = models.IntegerField()
    YoY_increase_in_sales = models.IntegerField()


class CompanyDebt(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='debts')
    tax_office_debt = models.IntegerField(default=0)
    social_insurance_agency_debt = models.IntegerField(default=0)
    health_insurance_company_debt = models.IntegerField(default=0)

    def __str__(self):
        return self.company_name
