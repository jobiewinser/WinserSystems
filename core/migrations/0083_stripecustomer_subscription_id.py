# Generated by Django 3.2.15 on 2022-12-27 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0082_auto_20221224_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripecustomer',
            name='subscription_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]