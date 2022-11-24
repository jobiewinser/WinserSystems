# Generated by Django 3.2.15 on 2022-10-19 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0004_remove_whatsapptemplate_latest_reason'),
        ('core', '0004_profile_calendly_org_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachedError',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('type', models.CharField(choices=[('1', 'You can only edit an active template once every 24 hours')], default='c', max_length=5)),
                ('attached_field', models.CharField(blank=True, max_length=50, null=True)),
                ('archived', models.BooleanField(default=False)),
                ('archived_time', models.DateTimeField(blank=True, null=True)),
                ('whatsapp_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='errors', to='whatsapp.whatsapptemplate')),
            ],
        ),
    ]