# Generated by Django 3.2.15 on 2022-11-20 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20221119_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='default_number',
        ),
    ]
