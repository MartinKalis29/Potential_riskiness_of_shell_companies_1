# Generated by Django 4.1.1 on 2024-08-08 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0005_alter_executive_executive_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydebt',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_debt', to='viewer.company'),
        ),
    ]