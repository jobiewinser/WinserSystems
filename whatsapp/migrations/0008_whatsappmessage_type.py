# Generated by Django 3.2.15 on 2022-10-28 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0007_auto_20221028_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='whatsappmessage',
            name='type',
            field=models.TextField(blank=True, null=True),
        ),
    ]
