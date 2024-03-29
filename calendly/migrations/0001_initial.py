# Generated by Django 3.2.15 on 2022-10-14 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20221014_1902'),
        ('campaign_leads', '0002_auto_20221014_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendlyWebhookRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('json_data', models.JSONField(blank=True, null=True)),
                ('request_type', models.CharField(choices=[('a', 'POST'), ('b', 'GET')], default='a', max_length=1)),
                ('booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='campaign_leads.booking')),
                ('errors', models.ManyToManyField(blank=True, null=True, to='core.ErrorModel')),
            ],
        ),
    ]
