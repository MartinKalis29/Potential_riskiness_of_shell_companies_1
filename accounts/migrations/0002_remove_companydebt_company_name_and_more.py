# Generated by Django 4.1.1 on 2024-08-09 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companydebt',
            name='company_name',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='employee_id_number',
            new_name='personal_id_number',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='personal_number',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='CompanyDebt',
        ),
    ]
