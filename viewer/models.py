from django.db import models


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date_of_foundation = models.IntegerField(null=True, blank=True)
    registered_office = models.CharField(max_length=255, default='Unknown Office')
    registered_office_city = models.CharField(max_length=255, default='Unknown City')
    executive = models.ForeignKey('Executive', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='companies')
    executive_year_of_change = models.IntegerField(null=True, blank=True, default=0)
    executive_change_count = models.IntegerField(null=True, blank=True, default=0)
    employee_count = models.IntegerField(null=True, blank=True, default=0)
    revenue_year = models.IntegerField(null=True, blank=True, default=0)
    YoY_increase_in_sales = models.IntegerField(null=True, blank=True, default=0)
    tax_office_debt = models.IntegerField(null=True, blank=True, default=0)
    social_insurance_agency_debt = models.IntegerField(null=True, blank=True, default=0)
    health_insurance_company_debt = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class Executive(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255, default='Unknown City')  # Predvolená hodnota
    date_of_change = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class RegisteredOffice(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.address}, {self.city}"


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.count} employees at {self.company.name}"


class Revenue(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='revenues')
    yearly_revenue = models.IntegerField(default=0)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.yearly_revenue} in {self.year}"


class CompanyDebt(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='debts')
    tax_office_debt = models.IntegerField(default=0)
    social_insurance_debt = models.IntegerField(default=0)
    health_insurance_debt = models.IntegerField(default=0)

    def __str__(self):
        return f"Debt for {self.company.name}"
