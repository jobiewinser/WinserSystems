# Generated by Django 3.2.15 on 2022-12-27 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_stripecustomer_subscription_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesubscriptionchange',
            name='processed',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
