# Generated by Django 3.2.15 on 2022-10-21 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20221020_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachederror',
            name='type',
            field=models.CharField(choices=[('1101', 'You can only edit an active template once every 24 hours'), ('1102', 'The system can not send Whatsapp Templates without a template name'), ('1103', 'The number of parameters submitted does not match the Whatsapp Template (contact Winser Systems)'), ('1201', "Whatsapp Template not found Whatsapp's system"), ('1202', "There is no Whatsapp Business linked to this Lead's assosciated Site"), ('1203', "There is no 1st Whatsapp Template linked to this Lead's assosciated Site"), ('1204', "There is no 2nd Whatsapp Template linked to this Lead's assosciated Site"), ('1205', "There is no 3rd Whatsapp Template linked to this Lead's assosciated Site")], default='c', max_length=5),
        ),
    ]
