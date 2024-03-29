# Generated by Django 3.2.15 on 2023-01-18 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0087_auto_20230104_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachederror',
            name='type',
            field=models.CharField(choices=[('0101', 'You can only edit an active template once every 24 hours'), ('0102', 'The system can not send Whatsapp Templates without a template name'), ('0103', 'The number of parameters submitted does not match the Whatsapp Template (contact Winser Systems)'), ('0104', 'the template has been deleted from Whatsapp Manager.'), ('1104', 'Message failed to send because more than 24 hours have passed since the customer last replied to this number. You can still send a template message at 24 hour intervals instead'), ('1105', 'Message failed to send because the Whatsapp account is not yet registered (contact Winser Systems)'), ('1106', 'The requested phone number has been deleted'), ('1107', "Parameter Invalid - They probably aren't on Whatsapp"), ('1108', "The message sent was too long (including any variables). Please edit the whatsapp template to make the offending section shorter or edit the lead/contact's name to be shorter for example."), ('1201', "Whatsapp Template not found Whatsapp's system"), ('1202', "There is no Whatsapp Business linked to this Lead's assosciated Site"), ('1203', "Couldn't auto-send, there is no 1st Whatsapp Template linked to this Lead's Campaign"), ('1220', 'This site has template messaging currently disabled, reenable it on the site configuration page'), ('1230', "This lead's campaign has no whatsapp number linked to it. Couldn't send first message"), ('1300', 'Unknown Error (We will investigate)'), ('1301', 'This template is missing a component'), ('1302', 'This template needs a name'), ('1303', "One of this template's sections is too long"), ('1304', 'A template with this name was recently deleted, please change the template name then try again')], default='c', max_length=5),
        ),
    ]
