import os
import django
import pytest

# Nastav environment variable DJANGO_SETTINGS_MODULE pred spustením testov
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SafeBusiness.settings')
django.setup()

# Ďalšie nastavenia testov môžu ísť sem
