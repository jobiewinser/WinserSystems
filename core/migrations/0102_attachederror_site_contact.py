# Generated by Django 3.2.15 on 2023-02-17 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0101_auto_20230217_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachederror',
            name='site_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='errors', to='core.sitecontact'),
        ),
    ]