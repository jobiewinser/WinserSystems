# Generated by Django 3.2.15 on 2022-10-17 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0002_rename_whatsappwebhook_whatsappwebhookrequest'),
        ('campaign_leads', '0002_auto_20221014_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='first_send_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_send_template_campaign', to='whatsapp.whatsapptemplate'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='second_send_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_send_template_campaign', to='whatsapp.whatsapptemplate'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='third_send_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third_send_template_campaign', to='whatsapp.whatsapptemplate'),
        ),
    ]
