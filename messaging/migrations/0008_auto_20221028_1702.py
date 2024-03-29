# Generated by Django 3.2.15 on 2022-10-28 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0007_auto_20221028_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='secure/message_images'),
        ),
        migrations.AlterField(
            model_name='messageimage',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='secure/message_image_thumnails'),
        ),
    ]
