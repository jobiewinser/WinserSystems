# Generated by Django 3.2.15 on 2022-12-01 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_leads', '0011_auto_20221127_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='type',
        ),
    ]
