# Generated by Django 3.2.15 on 2022-10-14 14:42

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsAppMessage',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='messaging.message')),
                ('wamid', models.TextField(blank=True, null=True)),
                ('conversationid', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('messaging.message',),
        ),
        migrations.CreateModel(
            name='WhatsAppWebhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('json_data', models.JSONField(blank=True, null=True)),
                ('request_type', models.CharField(choices=[('a', 'POST'), ('b', 'GET')], default='a', max_length=1)),
                ('errors', models.ManyToManyField(blank=True, null=True, to='core.ErrorModel')),
            ],
        ),
        migrations.CreateModel(
            name='WhatsappTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('send_order', models.IntegerField(blank=True, choices=[(0, 'Never'), (1, 'Send on Lead Creation'), (2, 'Send 24 Hrs after Lead Creation'), (3, 'Send 48 Hrs after Lead Creation')], default=0, null=True)),
                ('edited', models.DateTimeField(blank=True, null=True)),
                ('latest_reason', models.TextField(blank=True, null=True)),
                ('status', models.TextField(blank=True, null=True)),
                ('message_template_id', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('pending_name', models.TextField(blank=True, null=True)),
                ('category', models.TextField(blank=True, null=True)),
                ('pending_category', models.TextField(blank=True, null=True)),
                ('language', models.TextField(blank=True, null=True)),
                ('pending_language', models.TextField(blank=True, null=True)),
                ('components', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(default=dict), blank=True, default=[], null=True, size=None)),
                ('pending_components', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(default=dict), blank=True, default=[], null=True, size=None)),
                ('hidden', models.BooleanField(default=False)),
                ('archived', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.company')),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.site')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='WhatsAppMessageStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('raw_webhook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='whatsapp.whatsappwebhook')),
                ('whatsapp_message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='whatsapp.whatsappmessage')),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
        migrations.AddField(
            model_name='whatsappmessage',
            name='raw_webhook',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='whatsapp.whatsappwebhook'),
        ),
    ]