# Generated by Django 4.1.1 on 2024-08-08 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0006_alter_companydebt_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydebt',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_debts', to='viewer.company'),
        ),
    ]