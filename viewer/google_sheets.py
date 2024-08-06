import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .models import Company, Executive, CompanyDebt, RegisteredOffice, Employee, Revenue


def get_google_sheets_data(sheet_name):
    """
    Získa všetky údaje z Google Sheets na základe názvu tabuľky.

    :param sheet_name: Názov tabuľky v Google Sheets
    :return: Údaje zo všetkých riadkov v tabuľke ako zoznam slovníkov
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        r'C:\Users\hp\PycharmProjects\Potential_riskiness_of_shell_companies_1\arctic-carving-430707-s6-52ee32effc40.json',
        scope
    )
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # Predpokladáme, že sa používa prvý hárok
    data = sheet.get_all_records()
    return data


def update_companies_from_sheet(sheet_name):
    """
    Aktualizuje alebo vytvorí záznamy v databáze na základe údajov z Google Sheets.

    :param sheet_name: Názov tabuľky v Google Sheets
    """
    data = get_google_sheets_data(sheet_name)

    for item in data:
        # Update or create Executive
        executive, exec_created = Executive.objects.update_or_create(
            executive_name=item.get('executive_name'),
            defaults={
                'executive_address': item.get('executive_address'),
                'executive_city': item.get('executive_city'),
            }
        )

        # Update or create Company
        company, comp_created = Company.objects.update_or_create(
            company_id=item.get('company_id'),  # Používame company_id na zladenie existujúcich záznamov
            defaults={
                'company_name': item.get('company_name'),
                'year_of_foundation': item.get('year_of_foundation'),
                'executive_year_of_change': item.get('executive_year_of_change'),
                'executive_change_count': item.get('executive_change_count'),
            }
        )
        company.executives.add(executive)

        # Update or create RegisteredOffice
        RegisteredOffice.objects.update_or_create(
            registered_office_address=item.get('registered_office_address'),
            registered_office_city=item.get('registered_office_city'),
            company=company,
            defaults={
                'registered_office_address': item.get('registered_office_address'),
                'registered_office_city': item.get('registered_office_city'),
            }
        )

        # Update or create Employee
        Employee.objects.update_or_create(
            company=company,
            defaults={
                'employee_count': item.get('employee_count', 0),
            }
        )

        # Update or create Revenue
        Revenue.objects.update_or_create(
            company=company,
            defaults={
                'revenue_year': item.get('revenue_year', 0),
                'YoY_increase_in_sales': item.get('YoY_increase_in_sales', 0),
            }
        )

        # Update or create CompanyDebt
        CompanyDebt.objects.update_or_create(
            company=company,
            defaults={
                'tax_office_debt': item.get('tax_office_debt', 0),
                'social_insurance_agency_debt': item.get('social_insurance_agency_debt', 0),
                'health_insurance_company_debt': item.get('health_insurance_company_debt', 0),
            }
        )