# Generated by Django 3.2.15 on 2022-12-22 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_siteprofilepermissions_change_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofilepermissions',
            name='edit_site_calendly_configuration',
            field=models.BooleanField(default=False),
        ),
    ]