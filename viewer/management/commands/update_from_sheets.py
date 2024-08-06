from django.core.management.base import BaseCommand
from viewer.google_sheets import update_companies_from_sheet


class Command(BaseCommand):
    help = 'Update database from Google Sheets'

    def handle(self, *args, **kwargs):
        sheet_name = 'Database_companies'
        update_companies_from_sheet(sheet_name)
        self.stdout.write(self.style.SUCCESS('Successfully updated database from Google Sheets'))
