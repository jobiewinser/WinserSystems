# Generated by Django 3.2.15 on 2022-12-22 16:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0073_auto_20221222_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesubscriptionchange',
            name='profiles_to_keep',
        ),
        migrations.AddField(
            model_name='sitesubscriptionchange',
            name='users_to_keep',
            field=models.ManyToManyField(blank=True, null=True, related_name='site_subscription_change_users_to_keep', to=settings.AUTH_USER_MODEL),
        ),
    ]
