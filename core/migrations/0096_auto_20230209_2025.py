# Generated by Django 3.2.15 on 2023-02-09 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0095_profile_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='theme',
            field=models.CharField(default='light', max_length=5),
        ),
    ]
