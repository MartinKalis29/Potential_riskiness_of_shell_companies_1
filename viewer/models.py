from datetime import datetime

from django.db import models
from django.db.models import Model, CharField, IntegerField, ForeignKey, ManyToManyField, DateTimeField, DateField


class Company(Model):
    name = CharField(max_length=50)
    date_of_foundation = DateField(null=True)
    #registered_office = ManyToManyField("RegisteredOffice", blank=True, related_name="company")
    #employee = ForeignKey(Employee, on_delete=DO_NOTHING)
    #employee je väzba company-employee one to many

    def __str__(self):
        return self.name


class Executive(Model):
    name = CharField(max_length=50)
    address = CharField(max_length=50)
    date_of_change = DateField(null=True)

    def __str__(self):
        return self.name

# class RegisteredOffice(Model):
#     address = CharField(max_length=20)
#
#
# class Employee(Model):
#     employee_count = IntegerField(default=0)
#
#
# class Revenue(Model):
#     yearly_revenue = IntegerField(default=0)
#     year = IntegerField(default=0)
#
#
# class Company_debt(Model):
#     tax_office_debt = IntegerField(default=0)
#     social_insurance_debt = IntegerField(default=0)
#     health_insurance_debt = IntegerField(default=0)
