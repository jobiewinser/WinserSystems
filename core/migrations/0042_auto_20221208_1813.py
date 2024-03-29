# Generated by Django 3.2.15 on 2022-12-08 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_rename_toggle_toggle_active_campaign_siteprofilepermissions_toggle_active_campaign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteprofilepermissions',
            name='edit_user_permissions',
        ),
        migrations.CreateModel(
            name='CompanyProfilePermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edit_user_permissions', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.company')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
        ),
    ]
