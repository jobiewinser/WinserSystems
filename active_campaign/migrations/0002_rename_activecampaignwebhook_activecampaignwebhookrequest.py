# Generated by Django 3.2.15 on 2022-10-14 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('active_campaign', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActiveCampaignWebhook',
            new_name='ActiveCampaignWebhookRequest',
        ),
    ]