# Generated by Django 3.2.15 on 2022-12-03 22:40
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_leads', '0012_remove_booking_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='webhook_enabled',
            field=models.BooleanField(default=True),
        ),
    ]
