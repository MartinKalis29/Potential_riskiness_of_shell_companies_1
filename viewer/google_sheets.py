import gspread
from oauth2client.service_account import ServiceAccountCredentials
from viewer.models import Company


def get_google_sheets_data(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        r'C:\Users\hp\PycharmProjects\Potential_riskiness_of_shell_companies_1\arctic-carving-430707-s6-52ee32effc40.json',
        scope
    )

    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()

    return data


def update_companies_from_sheet(sheet_name):
    data = get_google_sheets_data(sheet_name)

    for item in data:
        Company.objects.update_or_create(
            name=item.get('company_name'),
            defaults={
                'date_of_foundation': item.get('date_of_foundation'),
                'registered_office': item.get('registered_office'),
                'registered_office_city': item.get('registered_office_city'),
                'executive_year_of_change': item.get('executive_year_of_change'),
                'executive_change_count': item.get('executive_change_count'),
                'employee_count': item.get('employee_count'),
                'revenue_year': item.get('revenue_year'),
                'YoY_increase_in_sales': item.get('YoY_increase_in_sales'),
                'tax_office_debt': item.get('tax_office_debt'),
                'social_insurance_agency_debt': item.get('social_insurance_agency_debt'),
                'health_insurance_company_debt': item.get('health_insurance_company_debt'),
            }
        )
