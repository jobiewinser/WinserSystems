# Generated by Django 3.2.15 on 2023-02-17 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0100_whatsappbusinessaccount_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='first_name',
            new_name='first_name_old',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='last_name',
            new_name='last_name_old',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='site',
            new_name='site_old',
        ),
        migrations.AddField(
            model_name='contact',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.company'),
        ),
        migrations.CreateModel(
            name='SiteContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('first_name_old', models.TextField(blank=True, max_length=25, null=True)),
                ('last_name_old', models.TextField(blank=True, max_length=25, null=True)),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.contact')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.site')),
            ],
        ),
    ]