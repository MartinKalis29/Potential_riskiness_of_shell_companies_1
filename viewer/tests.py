from django.test import TestCase

# Create your tests here.
from viewer.google_sheets import get_google_sheets_data

def test_get_google_sheets_data():
    sheet_name = "Database_companies"
    data = get_google_sheets_data(sheet_name)
    assert len(data) > 0  # Predpokladáme, že by malo byť viac ako 0 záznamov
    print(data)  # Tento príkaz môžeš odstrániť po úspešnom teste