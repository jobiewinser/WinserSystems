# Generated by Django 3.2.15 on 2022-10-28 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_leads', '0005_auto_20221023_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='call',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
