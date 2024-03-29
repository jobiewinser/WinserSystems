import logging
import os
import requests
from django.conf import settings
import json
from django.core.mail import send_mail


from whatsapp.models import WhatsappMessageImage, WhatsappTemplate
logger = logging.getLogger(__name__)
# https://developers.facebook.com/docs/whatsapp/cloud-api/reference
# https://business.facebook.com/settings/people/100085397745468?business_id=851701125750291
class Whatsapp():    
    # whatsapp_access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    whatsapp_url = os.getenv("WHATSAPP_URL")
    whatsapp_app_id = os.getenv("WHATSAPP_APP_ID")
    

    def __init__(self, whatsapp_access_token):
        self.whatsapp_access_token = whatsapp_access_token

    def _get_headers(self):
        headers = {
            'Authorization': 'Bearer ' + self.whatsapp_access_token,
                   'Content-Type': 'application/json'
                   }
        return headers
    #POST
    def send_free_text_message(self, customer_number, message, whatsapp_number, preview_url = False):   
        print("send_free_text_message", customer_number, message, whatsapp_number)
        from core.models import AttachedError
        if message:  
            if settings.WHATSAPP_PHONE_OVERRIDE1:
                non_overwritten_customer_number = customer_number
                customer_number = settings.WHATSAPP_PHONE_OVERRIDE1
            url = f"{self.whatsapp_url}/{whatsapp_number.whatsapp_business_phone_number_id}/messages"
            headers = self._get_headers()
            body = { 
                "messaging_product": "whatsapp", 
                "to": f"{customer_number}", 
                "type": "text",
                "text": json.dumps({
                    "body": f"{message}",
                    "preview_url": preview_url,
                    })
            }
            response = requests.post(url=url, json=body, headers=headers)
            response_body = response.json()
            attached_errors = []
            # response_body = {
            #     "object": "whatsapp_business_account",
            #     "entry": [
            #         {
            #             "id": "104128642479500",
            #             "changes": [
            #                 {
            #                     "value": {
            #                         "messaging_product": "whatsapp",
            #                         "metadata": {
            #                             "display_phone_number": "447872000364",
            #                             "phone_number_id": "108208485398311"
            #                         },
            #                         "statuses": [
            #                             {
            #                                 "id": "wamid.HBgMNDQ3ODI3Nzc3OTQwFQIAERgSNjgxNDQ4MjVENUM5NkY3NTc2AA==",
            #                                 "status": "failed",
            #                                 "timestamp": "1666789627",
            #                                 "recipient_id": "447827777940",
            #                                 "errors": [
            #                                     {
            #                                         "code": 131047,
            #                                         "title": "Message failed to send because more than 24 hours have passed since the customer last replied to this number.",
            #                                         "href": "https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes/"
            #                                     }
            #                                 ]
            #                             }
            #                         ]
            #                     },
            #                     "field": "messages"
            #                 }
            #             ]
            #         }
            #     ]
            # }
            for entry in response_body.get('entry', []):
                for change in entry.get('changes'):
                    value = change.get('value')
                    for status in value.get('statuses'):
                        potential_errors = status.get('errors', None)
                        if potential_errors:
                            for error in potential_errors:
                                code = error.get('code')
                                # I don't think this is useful, but leaving just in case




                                # if str(code) == '131047':
                                #     attached_errors.append(
                                #         AttachedError.objects.create(
                                #             type = '1104',
                                #             attached_field = "whatsapp_number",
                                #             whatsapp_number = whatsapp_number,
                                #             customer_number = non_overwritten_customer_number,
                                #         )
                                #     )                                
            # if not attached_errors:
            #     AttachedError.objects.filter(
            #         type__in = ['1104','1105'],
            #         archived = False,
            #         whatsapp_number = whatsapp_number,
            #         customer_number = non_overwritten_customer_number,
            #     ).update(archived = True)

            print("send_free_text_message response_body", response_body)
            return response_body, attached_errors
    def send_template_message(self, customer_number, whatsapp_number, template_object, language, components):  
        from core.models import AttachedError
        template_name = template_object.name
        #  "components": [{
        #     "type": "body",
        #     "parameters": [{
        #                     "type": "text",
        #                     "text": "name"
        #                 },
        #                 {
        #                 "type": "text",
        #                 "text": "Hi there"
        #                 }]
        #         }] 
        non_overwritten_customer_number = customer_number
        if settings.WHATSAPP_PHONE_OVERRIDE1:
            customer_number = settings.WHATSAPP_PHONE_OVERRIDE1
        if template_name:  
            AttachedError.objects.filter(
                type = '0102',
                whatsapp_template = template_object,
                customer_number = non_overwritten_customer_number,
                whatsapp_number = whatsapp_number,
                archived = False,
            ).update(archived = True)
            url = f"{self.whatsapp_url}/{whatsapp_number.whatsapp_business_phone_number_id}/messages"
            headers = self._get_headers()
            body = { 
                "messaging_product": "whatsapp", 
                "to": f"{customer_number}", 
                "type": "template",
                "template": json.dumps({
                    "name": template_name,
                    "language": language,
                    "components": components
                    })
            }
            print("")
            print("")
            print("send_template_message body", str(body))
            print("")
            print("")
            response = requests.post(url=url, json=body, headers=headers)
            response_body = response.json()
            
            from campaign_leads.models import Campaignlead            
            potential_error = response_body.get('error', None)
            if potential_error:
                code = potential_error.get('code')
                details = potential_error.get('details', "")
                
                campaign_lead = Campaignlead.objects.filter(whatsapp_number=non_overwritten_customer_number).last()
                if str(code) == '132000':
                    AttachedError.objects.create(
                        type = '0103',
                        attached_field = "whatsapp_template",
                        whatsapp_template = template_object,
                        campaign_lead=campaign_lead,
                        customer_number = non_overwritten_customer_number,
                        whatsapp_number = whatsapp_number,
                        admin_action_required = True,
                        additional_info = details,
                    )
                elif str(code) == '133010':
                    AttachedError.objects.create(
                        type = '1105',
                        attached_field = "whatsapp_template",
                        whatsapp_template = template_object,
                        campaign_lead=campaign_lead,
                        customer_number = non_overwritten_customer_number,
                        whatsapp_number = whatsapp_number,
                        admin_action_required = True,
                        additional_info = details,
                    )
                elif str(code) == '132005':
                    AttachedError.objects.create(
                        type = '1108',
                        attached_field = "whatsapp_template",
                        whatsapp_template = template_object,
                        campaign_lead=campaign_lead,
                        customer_number = non_overwritten_customer_number,
                        whatsapp_number = whatsapp_number,
                        admin_action_required = False,
                        additional_info = details,
                    )
                    
            else:
                AttachedError.objects.filter(
                    type__in = ['0103','1105','1108'],
                    whatsapp_template = template_object,
                    archived = False,
                    whatsapp_number = whatsapp_number,
                    customer_number = non_overwritten_customer_number,
                ).update(archived = True)

            print("send_template_message response_body", response_body)
            return response_body
        else:
            campaign_lead = Campaignlead.objects.filter(whatsapp_number=non_overwritten_customer_number).last()
            AttachedError.objects.create(
                type = '0102',
                attached_field = "whatsapp_template",
                whatsapp_template = template_object,
                        campaign_lead=campaign_lead,
                whatsapp_number = whatsapp_number,
                customer_number = non_overwritten_customer_number,
            )
    #POST
    def create_template(self, template_object):   
        from core.models import AttachedError
        url = f"{self.whatsapp_url}/{template_object.whatsapp_business_account.whatsapp_business_account_id}/message_templates"
        headers = self._get_headers()
        pending_components = template_object.pending_components
        for component in pending_components:
            counter = 1
            text = component.get('text', '')
            if text:
                if '[[1]]' in text:
                    text = text.replace('[[1]]','{{'+str(counter)+'}}')
                    counter = counter + 1
                component['text'] = text

        # for i in range(len(pending_components)):
        #     if not pending_components[i].get('text', ''):
        #         del pending_components[i]
        i = 0
        length = len(pending_components)
        while i < length:
            if not pending_components[i].get('text', ''):
                del pending_components[i]
                i -= 1
                length -= 1
            i += 1
            
        body = { 
            "name": template_object.pending_name or template_object.name,
            "category": template_object.pending_category or template_object.category,
            "language": "en_GB",
            "components": pending_components,
        }
        response = requests.post(url=url, json=body, headers=headers)
        response_body = response.json()
        description = f"<p>body: {str(body)}</p><br><p>response_body: {str(response_body)}</p>"
        send_mail(
            subject=f'Winser Systems {os.getenv("SITE_URL")} - create template ',
            message=description,
            from_email='jobiewinser@gmail.com',
            recipient_list=['jobiewinser@gmail.com'])
        print(response_body)
        template_object = WhatsappTemplate.objects.get(pk=template_object.pk)
        message_template_id = response_body.get('id')
        error = response_body.get('error')
        if error:
            error_types = {
                '2388043':'1301',
                '100':'1302',
                '2388040':'1303',
                '2388023':'1304',
                
            }
            code = str(error.get('code', ""))
            error_subcode = str(error.get('error_subcode', ""))
            if error_subcode:
                type = error_types.get(error_subcode, None)
            elif code:
                type = error_types.get(code, None)
            if not type:                
                send_mail(
                    subject=f'Winser Systems {os.getenv("SITE_URL")} - create template error unknown type ',
                    message=f"unknown error for template {str(template_object.pk)}: {str(error)}",
                    from_email='jobiewinser@gmail.com',
                    recipient_list=['jobiewinser@gmail.com'])
                type = '1300'
            attached_error, created = AttachedError.objects.get_or_create(
                type = type,
                whatsapp_template = template_object,
                attached_field = "whatsapp_template",
                archived = False,
            )
        elif message_template_id:
            AttachedError.objects.filter(
                type__in = ['1300', '1301', '1302', '1303', '0101','0104'],
                whatsapp_template = template_object,
                attached_field = "whatsapp_template",
                archived = False,
            ).update(archived = True)
            template_object.message_template_id = message_template_id
            template_object.save()
            return response_body
    #POST
    def edit_template(self, template_object):   
        if template_object.status in ["APPROVED", "REJECTED", "PAUSED"]:
            url = f"{self.whatsapp_url}/{template_object.message_template_id}"
            headers = self._get_headers()
            pending_components = template_object.pending_components
            for component in pending_components:
                counter = 1
                text = component.get('text', '')
                if '[[1]]' in text:
                    text = text.replace('[[1]]','{{'+str(counter)+'}}')
                    counter = counter + 1
                component['text'] = text
            body = { 
                "components": pending_components
            }
            response = requests.post(url=url, json=body, headers=headers)
            response_body = response.json()
            potential_error = response_body.get('error', None)
            from core.models import AttachedError
            if potential_error:
                code = potential_error.get('code')
                if str(code) == '100':
                    if potential_error.get('error_subcode') == 33:
                        error_type = '0104'
                        # name = template_object.pending_name or template_object.name
                        # version_int = check_last_two_and_return_version_int(name)
                        # if version_int:
                        #     name = name[:-1] + str(version_int + 1)
                        # else:
                        #     name = name + "_1"
                        # template_object.pending_name = (template_object.pending_name or template_object.name) + "_1"
                        # create_attempt = self.create_template(template_object)
                        # if create_attempt:
                        #     return create_attempt
                    else:
                        error_type = '0101'
                    AttachedError.objects.create(
                        type = error_type,
                        attached_field = "whatsapp_template",
                        whatsapp_template = template_object,
                    )
            else:
                AttachedError.objects.filter(
                    type__in = ['0101','0104'],
                    whatsapp_template = template_object,
                    archived = False,
                ).update(archived = True)
            
            print("edit_template", str(response_body))
            return response_body
    #GET
    def get_templates(self, whatsapp_business_account_id):   
        if whatsapp_business_account_id:  
            url = f"{self.whatsapp_url}/{whatsapp_business_account_id}/message_templates"
            headers = self._get_headers()
            response = requests.get(url=url, headers=headers)
            response_body = response.json()
            return response_body
            
    #GET
    def get_template(self, whatsapp_business_account_id, message_template_id):   
        if whatsapp_business_account_id:  
            url = f"{self.whatsapp_url}/{message_template_id}"
            headers = self._get_headers()
            response = requests.get(url=url, headers=headers)
            response_body = response.json()
            return response_body
    #DELETE
    def delete_template(self, whatsapp_business_account_id, template_name):   
        if whatsapp_business_account_id:  
            url = f"{self.whatsapp_url}/{whatsapp_business_account_id}/message_templates"
            headers = self._get_headers()
            body = { 
                "name": template_name,
            }
            response = requests.delete(url=url, json=body, headers=headers)
            response_body = response.json()
            return response_body
            
    def get_phone_numbers(self, whatsapp_business_account_id):        
        url = f"{self.whatsapp_url}/{whatsapp_business_account_id}/phone_numbers?access_token={self.whatsapp_access_token}"
        # headers = self._get_headers()
        response = requests.get(url=url)
        response_body = response.json()
        return response_body     
            
    def create_phone_number(self, whatsapp_business_account_id, cc, phone_number, migrate_phone_number=True):        
        url = f"{self.whatsapp_url}/{whatsapp_business_account_id}/phone_numbers"
        headers = self._get_headers()
        filtered_number = ""
        for c in phone_number:
            if c.isdigit():
                filtered_number = filtered_number + c
        body = { 
            "cc": cc, 
            "phone_number": filtered_number,
            "migrate_phone_number": str(migrate_phone_number).lower(), 
            "access_token": self.whatsapp_access_token, 
        }
        response = requests.post(url=url, json=body, headers=headers)
        response_body = response.json()
        return response_body        
            
    def get_media_url(self, media_id):        
        url = f"{self.whatsapp_url}/{media_id}"
        headers = self._get_headers()
        response = requests.get(url=url, headers=headers)
        response_body = response.json()
        return response_body
            
    def get_media_file(self, media_url):        
        url = f"{media_url}"
        headers = self._get_headers()
        response = requests.get(url=url, headers=headers)
        
        return response
            
    def get_media_file_from_media_id(self, media_id):        
        media_url = self.get_media_url(media_id).get('url') 
        response = self.get_media_file(media_url)
        filename = get_filename_from_cd(response.headers.get('content-disposition'))
        # file = open(filename, "wb")
        # file.write(response.content)
        # file.close()
        import io
        from django.core.files.images import ImageFile
        image = ImageFile(io.BytesIO(response.content), name=filename)  # << the answer!
        return image
            
    def get_business(self, whatsapp_business_id):     
        url = f"{self.whatsapp_url}/{whatsapp_business_id}"
        headers = self._get_headers()
        response = requests.get(url=url, headers=headers)
        response_body = response.json()
        return response_body

import re
def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


# def check_last_two_and_return_version_int(string):
#   if string[-2:] == '_':
#     try:
#       return int(string[-1])
#     except ValueError:
#       return False
#   else:
#     return False