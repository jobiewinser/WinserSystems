# Generated by Django 3.2.15 on 2023-02-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0094_alter_site_billing_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='color',
            field=models.CharField(default='96,248,61', max_length=15),
        ),
    ]
