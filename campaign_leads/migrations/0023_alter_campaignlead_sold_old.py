# Generated by Django 3.2.15 on 2023-01-06 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_leads', '0022_auto_20230104_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignlead',
            name='sold_old',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
