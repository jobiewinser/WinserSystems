# Generated by Django 3.2.15 on 2022-10-28 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0005_messageimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageimage',
            name='image',
            field=models.FileField(upload_to='secure/message_images/% Y/% m/% d/'),
        ),
    ]
