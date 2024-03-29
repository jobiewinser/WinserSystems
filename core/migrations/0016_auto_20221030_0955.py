# Generated by Django 3.2.15 on 2022-10-30 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_attachederror_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phonenumber',
            name='site',
        ),
        migrations.CreateModel(
            name='WhatsappBusinessAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp_business_account_id', models.TextField(blank=True, null=True)),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.site')),
            ],
        ),
        migrations.AddField(
            model_name='whatsappnumber',
            name='whatsapp_business_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.whatsappbusinessaccount'),
        ),
    ]
