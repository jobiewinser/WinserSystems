# Generated by Django 3.2.15 on 2022-12-20 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_auto_20221219_0424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('free', 'Free'), ('basic', 'Basic'), ('pro', 'Pro')], default='free', max_length=5)),
                ('max_users', models.IntegerField(default=0)),
                ('analytics_seconds', models.IntegerField(default=0)),
                ('subscription_link', models.TextField(blank=True, null=True)),
                ('numerical', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='site',
            name='subscription',
        ),
        migrations.AddField(
            model_name='site',
            name='subscription_old',
            field=models.CharField(default='free', max_length=5),
        ),
        migrations.AlterField(
            model_name='attachederror',
            name='type',
            field=models.CharField(choices=[('0101', 'You can only edit an active template once every 24 hours'), ('0102', 'The system can not send Whatsapp Templates without a template name'), ('0103', 'The number of parameters submitted does not match the Whatsapp Template (contact Winser Systems)'), ('1104', 'Message failed to send because more than 24 hours have passed since the customer last replied to this number. You can still send a template message at 24 hour intervals instead'), ('1105', 'Message failed to send because the Whatsapp account is not yet registered (contact Winser Systems)'), ('1106', 'The requested phone number has been deleted'), ('1107', "Parameter Invalid - They probably aren't on Whatsapp"), ('1108', "The message sent was too long (including any variables). Please edit the whatsapp template to make the offending section shorter or edit the lead/contact's name to be shorter for example."), ('1201', "Whatsapp Template not found Whatsapp's system"), ('1202', "There is no Whatsapp Business linked to this Lead's assosciated Site"), ('1203', "Couldn't auto-send, there is no 1st Whatsapp Template linked to this Lead's Campaign"), ('1220', 'This site has template messaging currently disabled, reenable it on the site configuration page'), ('1230', "This lead's campaign has no whatsapp number linked to it. Couldn't send first message"), ('1300', 'Unknown Error (We will investigate)'), ('1301', 'This template is missing a component'), ('1302', 'This template needs a name'), ('1303', "One of this template's sections is too long"), ('1304', 'A template with this name was recently deleted, please change the template name then try again')], default='c', max_length=5),
        ),
        migrations.CreateModel(
            name='SiteSubscriptionChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('completed', models.DateTimeField(blank=True, null=True)),
                ('canceled', models.DateTimeField(blank=True, null=True)),
                ('subscription_from_text', models.TextField(blank=True, null=True)),
                ('subscription_to_text', models.TextField(blank=True, null=True)),
                ('profiles_to_keep', models.ManyToManyField(blank=True, null=True, related_name='site_subscription_change_profiles_to_keep', to='core.Profile')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.site')),
                ('subscription_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='site_subscription_change_subscription_from', to='core.subscription')),
                ('subscription_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='site_subscription_change_subscription_to', to='core.subscription')),
            ],
        ),
        migrations.AddField(
            model_name='site',
            name='subscription_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.subscription'),
        ),
    ]
