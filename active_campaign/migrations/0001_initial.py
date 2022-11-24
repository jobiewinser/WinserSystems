# Generated by Django 3.2.15 on 2022-10-14 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campaign_leads', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveCampaignList',
            fields=[
                ('campaign_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='campaign_leads.campaign')),
                ('active_campaign_id', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('campaign_leads.campaign',),
        ),
        migrations.CreateModel(
            name='ActiveCampaignWebhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_data', models.JSONField(default=dict)),
                ('guid', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
