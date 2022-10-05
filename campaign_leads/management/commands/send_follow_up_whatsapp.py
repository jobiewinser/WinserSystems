import logging
from django.core.management.base import BaseCommand
from campaign_leads.models import Campaignlead, Booking, Call, Note, WhatsappTemplate
logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = 'help text'

    def handle(self, *args, **options):
        for campaign_lead in Campaignlead.objects.filter(booking=None).exclude(sold=True).exclude(complete=True).exclude(whatsappmessage__template__send_order=3):
            if not campaign_lead.whatsappmessage_set.filter(whatsappmessage__template__send_order=1):
                campaign_lead.send_whatsapp_message(whatsapp_template_send_order=1, user=None)
            elif not campaign_lead.whatsappmessage_set.filter(whatsappmessage__template__send_order=2):
                campaign_lead.send_whatsapp_message(whatsapp_template_send_order=2, user=None)
            else:
                campaign_lead.send_whatsapp_message(whatsapp_template_send_order=3, user=None)