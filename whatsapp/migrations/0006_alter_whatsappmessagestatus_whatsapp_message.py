# Generated by Django 3.2.15 on 2022-10-23 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0005_whatsapptemplate_last_approval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whatsappmessagestatus',
            name='whatsapp_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='whatsapp.whatsappmessage'),
        ),
    ]
