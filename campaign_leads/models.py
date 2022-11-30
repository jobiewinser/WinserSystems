from datetime import timedelta, datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse
from whatsapp.api import Whatsapp
from whatsapp.models import WhatsAppMessage, WhatsappTemplate
from django.dispatch import receiver
from polymorphic.models import PolymorphicModel
import logging
from django.db.models import Q, Count
from django.template import loader
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
logger = logging.getLogger(__name__)

BOOKING_CHOICES = (
                    ('a', 'In Person'),
                    ('b', 'Phone'),
                )
booking_choices_dict = {}
for tuple in BOOKING_CHOICES:
    booking_choices_dict[tuple[0]] = tuple[1]

# class AdCampaign(models.Model):
#     name = models.TextField(null=True, blank=True)

class Campaign(PolymorphicModel):
    name = models.TextField(null=True, blank=True)   
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    product_cost = models.FloatField(default=100)
    json_data = models.JSONField(default=dict)
    guid = models.TextField(null=True, blank=True)
    webhook_created = models.BooleanField(default=False)
    webhook_id = models.TextField(null=True, blank=True)
    site = models.ForeignKey('core.Site', on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey("core.Company", on_delete=models.SET_NULL, null=True, blank=True)
    first_send_template = models.ForeignKey("whatsapp.WhatsappTemplate", related_name="first_send_template_campaign", on_delete=models.SET_NULL, null=True, blank=True)
    second_send_template = models.ForeignKey("whatsapp.WhatsappTemplate", related_name="second_send_template_campaign", on_delete=models.SET_NULL, null=True, blank=True)
    third_send_template = models.ForeignKey("whatsapp.WhatsappTemplate", related_name="third_send_template_campaign", on_delete=models.SET_NULL, null=True, blank=True)
    fourth_send_template = models.ForeignKey("whatsapp.WhatsappTemplate", related_name="fourth_send_template_campaign", on_delete=models.SET_NULL, null=True, blank=True)
    fifth_send_template = models.ForeignKey("whatsapp.WhatsappTemplate", related_name="fifth_send_template_campaign", on_delete=models.SET_NULL, null=True, blank=True)
    whatsapp_business_account = models.ForeignKey('core.WhatsappBusinessAccount', on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(max_length=15, null=False, blank=False, default="96,248,61")
    def get_active_leads_qs(self):
        return self.campaignlead_set.filter(archived=False)
    def is_manual(self):
        return False
    @property
    def site_templates(self):
        return WhatsappTemplate.objects.filter(site=self.site)
    @property
    def warnings(self):
        warnings = {}
        if not self.first_send_template:
            warnings["first_send_template_missing"] = "This campaign doesn't have a 1st Auto-Send Template, it won't automatically send a message to the customer"
        return warnings
@receiver(models.signals.post_save, sender=Campaign)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.guid = str(uuid.uuid4())[:16]
        instance.save()

class ManualCampaign(Campaign):
    pass
    @property
    def is_manual(self):
        return True


class Campaignlead(models.Model):
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    
    whatsapp_number = models.TextField(null=True, blank=True)
    # country_code = models.TextField(null=True, blank=True)
    campaign = models.ForeignKey("campaign_leads.Campaign", on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    arrived = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    marked_sold = models.DateTimeField(null=True, blank=True)
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="campaignlead_sold_by", null=True, blank=True)
    archived = models.BooleanField(default=False)
    active_campaign_contact_id = models.TextField(null=True, blank=True)
    active_campaign_form_id = models.TextField(null=True, blank=True)
    possible_duplicate = models.BooleanField(default=False)
    last_dragged = models.DateTimeField(null=True, blank=True)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name
    @property
    def is_last_whatsapp_message_inbound(self):        
        message = WhatsAppMessage.objects.filter(customer_number=self.whatsapp_number, whatsappnumber__whatsapp_business_account__site=self.campaign.site).last()
        if message:
            return message.inbound
        return False
    @property
    def active_errors(self):        
        from core.models import AttachedError
        return AttachedError.objects.filter(Q(campaign_lead=self)|Q(customer_number=self.whatsapp_number, whatsapp_number__whatsapp_business_account__site=self.campaign.site)).filter(archived=False)
    @property
    def active_bookings(self):        
        return self.booking_set.exclude(archived=True)

    @property
    def name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def trigger_refresh_websocket(self, refresh_position=False):
        channel_layer = get_channel_layer()   
        if refresh_position:
            rendered_html = self.get_leads_html(new_position=Call.objects.filter(lead=self).count())
            async_to_sync(channel_layer.group_send)(
                f"lead_{self.campaign.site.company.pk}",
                {
                    'type': 'lead_update',
                    'data':{
                        'rendered_html':rendered_html,
                    }
                }
            )
        else:
            rendered_html = self.get_leads_html()
            async_to_sync(channel_layer.group_send)(
                f"lead_{self.campaign.site.company.pk}",
                {
                    'type': 'lead_update',
                    'data':{
                        'rendered_html':rendered_html,
                    }
                }
            )
    def get_leads_html(self, new_position=None):
        if self:
            if new_position == None:    
                rendered_html = f"<span hx-swap-oob='outerHTML:.lead-{self.pk}' hx-get='/campaign-leads/refresh-lead-article/{self.pk}/' hx-swap='outerHTML' hx-indicator='#top-htmx-indicator' hx-trigger='load' ></span>"
                return rendered_html
            else:
                delete_htmx = f"<span hx-swap-oob='delete' id='lead-{self.pk}'></span>"
                rendered_html = f"<span hx-swap-oob='afterbegin:.campaign_column_{self.campaign.pk}_calls_{new_position},.site_column_{self.campaign.site.pk}_calls_{new_position},.company_column_{self.campaign.site.company.pk}_calls_{new_position}'><a hx-get='/campaign-leads/refresh-lead-article/{self.pk}/' hx-swap='outerHTML' hx-indicator='#top-htmx-indicator' hx-trigger='load' href='#'></a> </span>"
                from django.utils.safestring import mark_safe
                return mark_safe(f"{rendered_html} {delete_htmx}")

    def send_template_whatsapp_message(self, whatsappnumber=None, send_order=None, template=None, communication_method = 'a'):
        print("Campaignlead send_template_whatsapp_message", whatsappnumber, send_order, template, communication_method)
        from core.models import AttachedError
        if communication_method == 'a':
            print("CampaignleadDEBUG1")
            if send_order == 1:
                template = self.campaign.first_send_template
                type = '1203'
            elif send_order == 2:
                template = self.campaign.second_send_template
                type = '1204'
            elif send_order == 3:
                template = self.campaign.third_send_template
                type = '1205'
            elif send_order == 4:
                template = self.campaign.fourth_send_template
                type = '1206'
            elif send_order == 5:
                template = self.campaign.fifth_send_template
                type = '1207'
            else:
                type = None
            
            if template:      
                print("CampaignleadDEBUG2")
                if type:          
                    AttachedError.objects.filter(
                        type = type,
                        campaign_lead = self,
                        archived = False,
                    ).update(archived = True)
                if template.whatsapp_business_account.whatsapp_business_account_id:  
                    print("CampaignleadDEBUG3")                  
                    AttachedError.objects.filter(
                        type = '1202',
                        campaign_lead = self,
                        archived = False,
                    ).update(archived = True)
                    if template.whatsapp_business_account.site.whatsapp_template_sending_enabled:
                        print("CampaignleadDEBUG4")
                        AttachedError.objects.filter(
                            type = '1220',
                            campaign_lead = self,
                            archived = False,
                        ).update(archived = True)
                        if template.message_template_id:
                            print("CampaignleadDEBUG5")
                            AttachedError.objects.filter(
                                type = '1201',
                                campaign_lead = self,
                                archived = False,
                            ).update(archived = True)
                            whatsapp = Whatsapp(self.campaign.site.whatsapp_access_token)
                            template_live = whatsapp.get_template(template.whatsapp_business_account.whatsapp_business_account_id, template.message_template_id)
                            print(template_live)
                            template.name = template_live['name']

                            template.category = template_live['category']
                            template.language = template_live['language']
                            template.save()

                            components =   [] 

                            whole_text = ""
                            counter = 1
                            for component in template.components:
                                params = []
                                component_type = component.get('type', "").lower()
                                # if component_type == 'header':
                                text = component.get('text', '')
                                if component_type in ['header', 'body']:
                                    if '[[1]]' in text:
                                        params.append(              
                                            {
                                                "type": "text",
                                                "text":  self.first_name
                                            }
                                        )
                                        text = text.replace('[[1]]',self.first_name)
                                        counter = counter + 1
                                # if '{{3}}' in text:
                                #     params.append(           
                                #         {
                                #             "type": "text",
                                #             "text":  self.campaign.company.company_name
                                #         }
                                #     )
                                # if '{{4}}' in text:
                                #     params.append(                   
                                #         {
                                #             "type": "text",
                                #             "text":  self.campaign.site.whatsapp_number
                                #         }
                                #     )
                                whole_text = f"""
                                    {whole_text} 
                                    {text}
                                """
                                if params:
                                    components.append(
                                        {
                                            "type": component_type,
                                            "parameters": params
                                        }
                                    )
                        else:
                            print("CampaignleadDEBUG6")
                            print("errorhere selected template not found on Whatsapp's system")
                            attached_error, created = AttachedError.objects.get_or_create(
                                type = '1201',
                                attached_field = "campaign_lead",
                                campaign_lead = self,
                            )
                            if not created:
                                attached_error.created = datetime.now()
                                attached_error.save()
                            return HttpResponse("Messaging Error: Couldn't find the specified template", status=400)
                    else:
                        print("CampaignleadDEBUG7")
                        print("errorhere template messaging disabled")
                        attached_error, created = AttachedError.objects.get_or_create(
                            type = '1220',
                            attached_field = "campaign_lead",
                            campaign_lead = self,
                        )
                        if not created:
                            attached_error.created = datetime.now()
                            attached_error.save()
                        return HttpResponse("Messaging Error: Template Messaging disabled for this site", status=400)
                else:
                    print("CampaignleadDEBUG8")
                    print("errorhere no Whatsapp Business Account Linked")
                    attached_error, created = AttachedError.objects.get_or_create(
                        type = '1202',
                        attached_field = "campaign_lead",
                        campaign_lead = self,
                    )
                    if not created:
                        attached_error.created = datetime.now()
                        attached_error.save()
                    return HttpResponse("Messaging Error: No Whatsapp Business Account linked", status=400)
                language = {
                    "policy":"deterministic",
                    "code":template.language
                }
                site = self.campaign.site
                if not whatsappnumber and send_order:
                    whatsappnumber = self.campaign.whatsapp_business_account.whatsappnumber
                customer_number = self.whatsapp_number
                response = whatsapp.send_template_message(self.whatsapp_number, whatsappnumber, template, language, components)
                print(str(response))
                logger.debug(str(response))
                
                reponse_messages = response.get('messages',[])
                error = response.get('error',[])
                if reponse_messages:
                    AttachedError.objects.filter(
                        type__in = ['1107','1106'], 
                        attached_field = "campaign_lead",
                        campaign_lead = self,
                        archived = False,
                    ).update(archived = True)    
                    for response_message in reponse_messages:
                        whatsapp_message, created = WhatsAppMessage.objects.get_or_create(
                            wamid=response_message.get('id'),
                            datetime=datetime.now(),
                            lead=self,
                            message=whole_text,
                            site=site,
                            whatsappnumber=whatsappnumber,
                            customer_number=customer_number,
                            template=template,
                            inbound=False,
                            send_order=send_order
                        )
                        if created:                        
                            channel_layer = get_channel_layer()                            
                            message_context = {
                                "message": whatsapp_message,
                                "site": site,
                                "whatsappnumber": whatsappnumber,
                            }
                            rendered_message_list_row = loader.render_to_string('messaging/htmx/message_list_row.html', message_context)
                            rendered_message_chat_row = loader.render_to_string('messaging/htmx/message_chat_row.html', message_context)
                            rendered_html = f"""

                            <span id='latest_message_row_{customer_number}' hx-swap-oob='delete'></span>
                            <span id='messageCollapse_{whatsappnumber.pk}' hx-swap-oob='afterbegin'>{rendered_message_list_row}</span>

                            <span id='messageWindowInnerBody_{customer_number}' hx-swap-oob='beforeend'>{rendered_message_chat_row}</span>
                            """
                            
                            async_to_sync(channel_layer.group_send)(
                                f"messaging_{whatsappnumber.pk}",
                                {
                                    'type': 'chatbox_message',
                                    "message": rendered_html,
                                }
                            )
                            channel_layer = get_channel_layer()   
                            
                            async_to_sync(channel_layer.group_send)(
                                f"message_count_{whatsappnumber.site.company.pk}",
                                {
                                    'type': 'messages_count_update',
                                    'data':{
                                        'rendered_html':f"""<span hx-swap-oob="afterbegin:.company_message_count"><span hx-trigger="load" hx-swap="none" hx-get="/update-message-counts/"></span>""",
                                    }
                                }
                            )
                    logger.debug("site.send_template_whatsapp_message success") 
                    self.trigger_refresh_websocket(refresh_position=False)
                    return HttpResponse("Message Sent", status=200)
                    
                elif error.get('code', None) == 33:
                    AttachedError.objects.create(
                        type = '1106',
                        attached_field = "customer_number",
                        whatsapp_number = whatsappnumber,
                        customer_number = customer_number,
                        admin_action_required = True,
                    )
                elif error.get('code', None) == 100:   
                    attached_error, created = AttachedError.objects.get_or_create(
                        type = '1107',
                        attached_field = "campaign_lead",
                        campaign_lead = self,
                    )
                    self.trigger_refresh_websocket(refresh_position=False)
                    return HttpResponse("Message Not Sent", status=400)
                else:     
                    self.trigger_refresh_websocket(refresh_position=False)
                    return HttpResponse("Message Sent", status=500)
            else:
                print("CampaignleadDEBUG10")
                if send_order == 1:
                    type = '1203'
                elif send_order == 2:
                    type = '1204'
                elif send_order == 3:
                    type = '1205'
                elif send_order == 4:
                    type = '1206'
                elif send_order == 5:
                    type = '1207'
                print("errorhere no suitable template found")
                attached_error, created = AttachedError.objects.get_or_create(
                    type = type,
                    attached_field = "campaign_lead",
                    campaign_lead = self,
                )
                if not created:
                    print("CampaignleadDEBUG11")
                    attached_error.created = datetime.now()
                    attached_error.save()
        return HttpResponse("Message Error", status=400)
            
            

            
        # return HttpResponse("No Communication method specified", status=500)

@receiver(models.signals.post_save, sender=Campaignlead)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created and not instance.archived:
        try:
            instance.send_template_whatsapp_message(send_order=1)
        except:
            pass
        
class Call(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    datetime = models.DateTimeField(null=False, blank=False)
    lead = models.ForeignKey(Campaignlead, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    error_json = models.JSONField(default=dict)
    archived = models.BooleanField(default=False)
    class Meta:
        ordering = ['-datetime']

class Booking(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    lead = models.ForeignKey(Campaignlead, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(choices=BOOKING_CHOICES, max_length=2, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    calendly_event_uri = models.TextField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    class Meta:
        ordering = ['-datetime']

class Note(models.Model):
    text = models.TextField(null=False, blank=False)
    lead = models.ForeignKey(Campaignlead, on_delete=models.SET_NULL, null=True, blank=True)
    call = models.ForeignKey('campaign_leads.Call', on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #This referes to the date it was created unless it's attached to a call/booking, then it's set to the related datetime
    datetime = models.DateTimeField(null=True, blank=True) 
    class Meta:
        ordering = ['-datetime']

# try:
#     template, created = WhatsappTemplate.objects.get_or_create(pk=1)
#     template.name = "Immediate Lead Followup"
#     template.save()

#     template, created = WhatsappTemplate.objects.get_or_create(pk=2)
#     template.name = "Second Lead Followup"
#     template.save()

#     template, created = WhatsappTemplate.objects.get_or_create(pk=3)
#     template.name = "Third Lead Followup"
#     template.save()
# except:
#     pass