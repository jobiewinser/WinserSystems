# Generated by Django 3.2.15 on 2022-10-21 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0004_remove_whatsapptemplate_latest_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='whatsapptemplate',
            name='last_approval',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
