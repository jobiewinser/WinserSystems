# Generated by Django 3.2.15 on 2022-12-08 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_rename_company_name_company_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyprofilepermissions',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterModelOptions(
            name='siteprofilepermissions',
            options={'ordering': ['-pk']},
        ),
    ]
