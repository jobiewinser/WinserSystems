from django.shortcuts import render

from datetime import datetime, timezone
import logging
from django.conf import settings
from django.http import HttpResponse, QueryDict
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pytz
from calendly.api import Calendly
from calendly.models import CalendlyWebhookRequest
from campaign_leads.models import Booking, Campaignlead, Call
from whatsapp.api import Whatsapp
from django.views.generic import TemplateView
from whatsapp.models import WHATSAPP_ORDER_CHOICES, WhatsAppMessage, WhatsAppMessageStatus, WhatsAppWebhookRequest, WhatsappTemplate, template_variables
from django.template import loader
logger = logging.getLogger(__name__)
from django.views import View 
from django.utils.decorators import method_decorator
from core.models import ErrorModel, Site
from asgiref.sync import async_to_sync, sync_to_async

@method_decorator(csrf_exempt, name="dispatch")
class Webhooks(View):
    def get(self, request, *args, **kwargs):
        logger.debug(str(request.GET))
        challenge = request.GET.get('hub.challenge',{})
        response = HttpResponse(challenge)
        response.status_code = 200
        return response

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        print(str(body))
        logger.debug(str(body))
           
        webhook = CalendlyWebhookRequest.objects.create(
            json_data=body,
            request_type='a',
        )
        booking = Booking.objects.get(calendly_event_uri=body.get('payload').get('event'))
        calendly = Calendly(booking.lead.campaign.site.calendly_token)
        updated_booking_details_1 = calendly.get_from_uri(body.get('payload').get('uri'))
        start_time = datetime.strptime(updated_booking_details_1['resource']['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        timezone = pytz.timezone("GMT")
        start_time = timezone.localize(start_time)

        booking.datetime = start_time
        booking.save()

        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()          
        lead = booking.lead
        print(lead.campaign.site.company.all()[0].pk)
        campaign_pk = lead.campaign.site.company.all()[0].pk
        async_to_sync(channel_layer.group_send)(
            f"lead_{campaign_pk}",
            {
                'type': 'lead_update',
                'data':{
                    # 'company_pk':campaign_pk,
                    'lead_pk':lead.pk,
                }
            }
        )
        

        response = HttpResponse()
        response.status_code = 200
        return response

def calendly_booking_success(request):
    lead = Campaignlead.objects.get(pk = request.POST['lead_pk'])
    uri = request.POST['uri']
    if lead.campaign.site.company.all()[0] == request.user.profile.get_company:
        Booking.objects.get_or_create(user=request.user, calendly_event_uri=uri, lead=lead)
    return HttpResponse("", status=200)