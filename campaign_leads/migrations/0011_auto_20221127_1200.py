# Generated by Django 3.2.15 on 2022-11-27 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0013_auto_20221119_2337'),
        ('campaign_leads', '0010_rename_complete_campaignlead_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='fifth_send_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fifth_send_template_campaign', to='whatsapp.whatsapptemplate'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='fourth_send_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fourth_send_template_campaign', to='whatsapp.whatsapptemplate'),
        ),
    ]