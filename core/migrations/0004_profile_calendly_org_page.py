# Generated by Django 3.2.15 on 2022-10-18 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20221017_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='calendly_org_page',
            field=models.TextField(blank=True, null=True),
        ),
    ]
