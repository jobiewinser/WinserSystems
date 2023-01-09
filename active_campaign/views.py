import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from campaign_leads.models import Campaign, Campaignlead
from active_campaign.models import ActiveCampaignWebhookRequest, ActiveCampaign
from core.models import Site
logger = logging.getLogger(__name__)
from django.views import View 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from datetime import datetime, timedelta, time
from core.user_permission_functions import *
@method_decorator(csrf_exempt, name="dispatch")
class Webhooks(View):
    def get(self, request, *args, **kwargs):
        logger.debug(str(request.GET))
        return HttpResponse( "text", 200)

    def post(self, request, *args, **kwargs): 
        # try:
            logger.debug(str(request.POST))     
            data = request.POST  
            guid = kwargs.get('guid')
            if not data.get('initiated_by') == 'admin':
                ActiveCampaignWebhookRequest.objects.create(json_data = data, meta_data = str(request.META), guid=guid)       
                if data.get('type') in ['subscribe','update']:
                    if guid:
                        campaign = ActiveCampaign.objects.get(guid=guid)
                        if campaign.site:
                            if campaign.site.active_campaign_leads_enabled:
                                phone_number_whole = str(data.get('contact[phone]', "")).replace(' ','').replace('+','')

                                # possible_duplicate  = False
                                # today = datetime.now().date()
                                # tomorrow = today + timedelta(1)
                                # today_start = datetime.combine(today, time())
                                # today_end = datetime.combine(tomorrow, time())
                                campaign_lead, created = Campaignlead.objects.get_or_create(
                                        active_campaign_contact_id=data.get('contact[id]'),
                                        campaign=campaign,
                                    )
                                campaign_lead.first_name=data.get('contact[first_name]', "None")
                                campaign_lead.whatsapp_number=phone_number_whole
                                campaign_lead.active_campaign_form_id=data.get('form[id]', None)
                                campaign_lead.email = data.get('contact[email]', "")
                                
                                campaign_lead.save()
                                campaign_lead.trigger_refresh_websocket(refresh_position=True)
            return HttpResponse( "text", 200)
     
logger = logging.getLogger(__name__)
    

@login_required
def set_campaign_site(request, **kwargs):
    try:
        campaign = Campaign.objects.get(pk=kwargs.get('campaign_pk'))
        site_pk = request.POST.get('site_pk',None)
        campaign.campaigntemplatelink_set.all().delete()

        if site_pk:
            site = Site.objects.get(pk=site_pk)
            campaign.site = site
        else:
            campaign.site = None
        campaign.save()
        return render(request, 'campaign_leads/campaign_configuration_row.html', {'campaign':campaign,})
    except Exception as e:        
        logger.error(f"set_campaign_site {str(e)}")
        return HttpResponse("Couldn't set Campaign Site", status=500)

@login_required
def set_whatsapp_template_sending_status(request, **kwargs):
    try:
        site = Site.objects.get(pk=request.POST.get('site_pk',None))
        if get_profile_allowed_to_toggle_whatsapp_sending(request.user.profile, site):
            site.whatsapp_template_sending_enabled = request.POST.get('whatsapp_template_sending_enabled', 'off') == 'on'
            site.save()
            return render(request, 'core/htmx/whatsapp_template_sending_enabled_htmx.html', {'site':site,})
        return HttpResponse(status=403)
    except Exception as e:        
        logger.error(f"set_whatsapp_template_sending_status {str(e)}")
        return HttpResponse("Couldn't set_whatsapp_template_sending_status", status=500)

@login_required
def set_active_campaign_leads_status(request, **kwargs):
    try:
        site = Site.objects.get(pk=request.POST.get('site_pk',None))
        if get_profile_allowed_to_toggle_active_campaign(request.user.profile, site):
            site.active_campaign_leads_enabled = request.POST.get('active_campaign_leads_enabled', 'off') == 'on'
            site.save()
            return render(request, 'core/htmx/active_campaign_enabled_htmx.html', {'site':site,})
        return HttpResponse(status=403)
    except Exception as e:        
        logger.error(f"set_active_campaign_leads_status {str(e)}")
        return HttpResponse("Couldn't set_active_campaign_leads_status", status=500)

