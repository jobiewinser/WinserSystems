# Generated by Django 3.2.15 on 2022-12-16 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_rename_theme_colour_profile_demo_account_theme_colour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='demo_account_theme_colour',
            field=models.CharField(blank=True, default='', max_length=15, null=True),
        ),
    ]
