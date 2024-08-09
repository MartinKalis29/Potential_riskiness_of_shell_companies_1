from django.test import TestCase
from viewer.views import ExecutiveModelForm, CompanyModelForm
from viewer.models import Executive


class ExecutiveModelFormTest(TestCase):

    def test_executive_form_is_valid(self):
        form = ExecutiveModelForm(data={
            'executive_name': '   Jozef Novák   ',
            'executive_address': 'Hlavná 12',
            'executive_city': 'Bratislava'
        })
        print(f"test_executive_form_is_valid: {form.data}")
        self.assertTrue(form.is_valid())

    def test_executive_form_is_not_valid_blank_name(self):
        form = ExecutiveModelForm(data={
            'executive_name': '',
            'executive_address': 'Hlavná 12',
            'executive_city': 'Bratislava'
        })
        print(f"test_executive_form_is_not_valid_blank_name: {form.data}")
        self.assertFalse(form.is_valid())

    def test_executive_form_is_not_valid_blank_address(self):
        form = ExecutiveModelForm(data={
            'executive_name': 'Jozef Novák',
            'executive_address': '',
            'executive_city': 'Bratislava'
        })
        print(f"test_executive_form_is_not_valid_blank_address: {form.data}")
        self.assertFalse(form.is_valid())

    def test_executive_form_is_not_valid_blank_city(self):
        form = ExecutiveModelForm(data={
            'executive_name': 'Jozef Novák',
            'executive_address': 'Hlavná 12',
            'executive_city': ''
        })
        print(f"test_executive_form_is_not_valid_blank_city: {form.data}")
        self.assertFalse(form.is_valid())


class CompanyModelFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create initial data for the tests
        cls.executive1 = Executive.objects.create(
            executive_name="Pavol Kováč",
            executive_address="Liptovská 45",
            executive_city="Bratislava"
        )
        cls.executive2 = Executive.objects.create(
            executive_name="Mária Kováčová",
            executive_address="Košická 87",
            executive_city="Bratislava"
        )

    def test_company_form_is_valid(self):
        form = CompanyModelForm(data={
            'company_name': '   Sample Company   ',
            'year_of_foundation': 2023,
            'executives': [self.executive1.id, self.executive2.id],
            'executive_year_of_change': 2024,
            'executive_change_count': 3,
            'registered_office_address': 'Business Park 1000',
            'registered_office_city': 'Bratislava',
            'employee_count': 10,
            'revenue_year': 2023,
            'YoY_increase_in_sales': 15,
            'tax_office_debt': 1000,
            'social_insurance_agency_debt': 500,
            'health_insurance_company_debt': 300,
        })
        print(f"test_company_form_is_valid: {form.data}")
        self.assertTrue(form.is_valid())

    def test_company_form_is_not_valid_blank_name(self):
        form = CompanyModelForm(data={
            'company_name': '',
            'year_of_foundation': 2023,
            'executives': [self.executive1.id, self.executive2.id],
            'executive_year_of_change': 2024,
            'executive_change_count': 3,
            'registered_office_address': 'Business Park 1000',
            'registered_office_city': 'Bratislava',
            'employee_count': 10,
            'revenue_year': 2023,
            'YoY_increase_in_sales': 15,
            'tax_office_debt': 1000,
            'social_insurance_agency_debt': 500,
            'health_insurance_company_debt': 300,
        })
        print(f"test_company_form_is_not_valid_blank_name: {form.data}")
        self.assertFalse(form.is_valid())

    def test_company_form_is_not_valid_invalid_year_of_foundation(self):
        form = CompanyModelForm(data={
            'company_name': 'Sample Company',
            'year_of_foundation': 'invalid_year',  # Invalid year
            'executives': [self.executive1.id, self.executive2.id],
            'executive_year_of_change': 2024,
            'executive_change_count': 3,
            'registered_office_address': 'Business Park 1000',
            'registered_office_city': 'Bratislava',
            'employee_count': 10,
            'revenue_year': 2023,
            'YoY_increase_in_sales': 15,
            'tax_office_debt': 1000,
            'social_insurance_agency_debt': 500,
            'health_insurance_company_debt': 300,
        })
        print(f"test_company_form_is_not_valid_invalid_year_of_foundation: {form.data}")
        self.assertFalse(form.is_valid())

    def test_company_form_is_not_valid_future_revenue_year(self):
        form = CompanyModelForm(data={
            'company_name': 'Sample Company',
            'year_of_foundation': 2023,
            'executives': [self.executive1.id, self.executive2.id],
            'executive_year_of_change': 2024,
            'executive_change_count': 3,
            'registered_office_address': 'Business Park 1000',
            'registered_office_city': 'Bratislava',
            'employee_count': 10,
            'revenue_year': 2024,  # Invalid future year
            'YoY_increase_in_sales': 15,
            'tax_office_debt': 1000,
            'social_insurance_agency_debt': 500,
            'health_insurance_company_debt': 300,
        })
        print(f"test_company_form_is_not_valid_future_revenue_year: {form.data}")
        self.assertFalse(form.is_valid())

    def test_company_form_is_not_valid_negative_employee_count(self):
        form = CompanyModelForm(data={
            'company_name': 'Sample Company',
            'year_of_foundation': 2023,
            'executives': [self.executive1.id, self.executive2.id],
            'executive_year_of_change': 2024,
            'executive_change_count': 3,
            'registered_office_address': 'Business Park 1000',
            'registered_office_city': 'Bratislava',
            'employee_count': -5,  # Invalid negative count
            'revenue_year': 2023,
            'YoY_increase_in_sales': 15,
            'tax_office_debt': 1000,
            'social_insurance_agency_debt': 500,
            'health_insurance_company_debt': 300,
        })
        print(f"test_company_form_is_not_valid_negative_employee_count: {form.data}")
        self.assertFalse(form.is_valid())

    def test_company_form_is_not_valid_negative_debt(self):
        form = CompanyModelForm(data={
            'company_name': 'Sample Company',
            'year_of_foundation': 2023,
            'executives': [self.executive1.id, self.executive2.id],
            'executive_year_of_change': 2024,
            'executive_change_count': 3,
            'registered_office_address': 'Business Park 1000',
            'registered_office_city': 'Bratislava',
            'employee_count': 10,
            'revenue_year': 2023,
            'YoY_increase_in_sales': 15,
            'tax_office_debt': -1000,  # Invalid negative debt
            'social_insurance_agency_debt': 500,
            'health_insurance_company_debt': 300,
        })
        print(f"test_company_form_is_not_valid_negative_debt: {form.data}")
        self.assertFalse(form.is_valid())
