from django.test import TestCase
from viewer.models import *


class CompanyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        executive1 = Executive.objects.create(
            executive_name="Jozef Novák",
            executive_address="Novákova 123",
            executive_city="Bratislava"
        )
        executive2 = Executive.objects.create(
            executive_name="Mária Kováčová",
            executive_address="Kováčova 456",
            executive_city="Košice"
        )
        company = Company.objects.create(
            company_name="Originálny Názov",
            year_of_foundation=2021,
            executive_year_of_change=2021,
            executive_change_count=1
        )
        company.executives.add(executive1)
        company.executives.add(executive2)

        RegisteredOffice.objects.create(
            registered_office_address="Hlavná 1",
            registered_office_city="Bratislava",
            company=company
        )

        Employee.objects.create(
            employee_count=50,
            company=company
        )

        Revenue.objects.create(
            revenue_year=2022,
            YoY_increase_in_sales=10,
            company=company
        )

        CompanyDebt.objects.create(
            tax_office_debt=5000,
            social_insurance_agency_debt=3000,
            health_insurance_company_debt=2000,
            company=company
        )

    def setUp(self):
        print('-' * 80)

    def test_company_str(self):
        company = Company.objects.get(company_id=1)
        print(f"test_company_str: {company}")
        self.assertEqual(company.__str__(), "Originálny Názov")

    def test_company_executives(self):
        company = Company.objects.get(company_id=1)
        number_of_executives = company.executives.count()
        print(f"test_company_executives: {number_of_executives}")
        self.assertEqual(number_of_executives, 2)

    def test_registered_office_str(self):
        registered_office = RegisteredOffice.objects.get(id=1)
        print(f"test_registered_office_str: {registered_office}")
        self.assertEqual(registered_office.__str__(), "Hlavná 1, Bratislava")

    def test_employee_count(self):
        company = Company.objects.get(company_id=1)
        employee = company.employees.get(id=1)
        print(f"test_employee_count: {employee.employee_count}")
        self.assertEqual(employee.employee_count, 50)

    def test_revenue_yoy_increase(self):
        revenue = Revenue.objects.get(id=1)
        print(f"test_revenue_yoy_increase: {revenue.YoY_increase_in_sales}")
        self.assertEqual(revenue.YoY_increase_in_sales, 10)

    def test_company_debt_values(self):
        company_debt = CompanyDebt.objects.get(id=1)
        print(f"test_company_debt_values: Tax office debt: {company_debt.tax_office_debt}, "
              f"Social insurance debt: {company_debt.social_insurance_agency_debt}, "
              f"Health insurance debt: {company_debt.health_insurance_company_debt}")
        self.assertEqual(company_debt.tax_office_debt, 5000)
        self.assertEqual(company_debt.social_insurance_agency_debt, 3000)
        self.assertEqual(company_debt.health_insurance_company_debt, 2000)