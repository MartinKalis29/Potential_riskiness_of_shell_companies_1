from django.db import models


class Executive(models.Model):
    executive_name = models.CharField(max_length=255)
    executive_address = models.CharField(max_length=255)
    executive_city = models.CharField(max_length=255, default='Unknown City')
    executive_year_of_change = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.executive_name


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    year_of_foundation = models.IntegerField(null=True, blank=True)
    registered_office = models.CharField(max_length=255, default='Unknown Office')
    registered_office_city = models.CharField(max_length=255, default='Unknown City')
    executive = models.ForeignKey(Executive, on_delete=models.SET_NULL, null=True, blank=True, related_name='companies')
    executive_year_of_change = models.IntegerField(null=True, blank=True, default=0)
    executive_change_count = models.IntegerField(null=True, blank=True, default=0)
    employee_count = models.IntegerField(null=True, blank=True, default=0)
    revenue_year = models.IntegerField(null=True, blank=True, default=0)
    YoY_increase_in_sales = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.company_name


class RegisteredOffice(models.Model):
    registered_office = models.CharField(max_length=255)
    registered_office_city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.registered_office}, {self.registered_office_city}"


class Employee(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    employee_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.employee_count} employees at {self.company_name}"


class Revenue(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='revenues')
    revenue_year = models.IntegerField(default=0)
    YoY_increase_in_sales = models.IntegerField()

    def __str__(self):
        return f"{self.YoY_increase_in_sales} in {self.revenue_year}"


class CompanyDebt(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='debts')
    tax_office_debt = models.IntegerField(default=0)
    social_insurance_agency_debt = models.IntegerField(default=0)
    health_insurance_company_debt = models.IntegerField(default=0)

    def __str__(self):
        return f"Debt for {self.company_name}"
