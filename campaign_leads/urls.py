from django.urls import path
import campaign_leads.views as campaignleadsviews
import campaign_leads.htmx as campaignleadshtmx
urlpatterns = [
    


    path('refresh-booking-table/', campaignleadsviews.refresh_booking_table_htmx, name='refresh-booking-table'),
    path('booking-overview/', campaignleadsviews.CampaignBookingsOverviewView.as_view(), name='campaign-booking-overview'),
    path('refresh-leads-board/', campaignleadsviews.refresh_leads_board, name='refresh-leads-board'),
    path('leads-and-calls/', campaignleadsviews.CampaignleadsOverviewView.as_view(), name='campaign-leads-overview'),    




    path('configuration/campaign-configuration/', campaignleadsviews.CampaignConfigurationView.as_view(), name='campaign-configuration'),
    

    
    path('mark-archived/', campaignleadshtmx.mark_archived, name='mark-archived' ),
    path('mark-archived/<str:lead_pk>/', campaignleadshtmx.mark_archived, name='mark-archived' ),
    
    path('new-leads-column/', campaignleadshtmx.new_leads_column, name='new-leads-column' ),
    path('delete-lead/', campaignleadshtmx.delete_lead, name='delete-lead' ),
    
    path('refresh-lead-article/<str:lead_pk>/', campaignleadshtmx.refresh_lead_article, name='refresh-lead-article' ),
    path('refresh-booking-row/<str:lead_pk>/', campaignleadshtmx.refresh_booking_row, name='refresh-booking-row' ),
    path('toggle-claim-lead/<str:lead_pk>/', campaignleadsviews.toggle_claim_lead, name='toggle-claim-lead' ),
    # path('get-leads-column-meta-data/', campaignleadshtmx.get_leads_column_meta_data, name='get-leads-column-meta-data' ),
    # path('create-campaign-lead/', campaignleadshtmx.create_campaign_lead, name='create-campaign-lead' ),
    
    path('get-campaign/', campaignleadsviews.get_campaigns, name='get-campaign'),
    
    path('add-manual-booking/', campaignleadshtmx.add_manual_booking, name='add-manual-booking' ),
    path('mark-arrived/', campaignleadshtmx.mark_arrived, name='mark-arrived' ),
    path('mark-sold/', campaignleadshtmx.mark_sold, name='mark-sold' ),
    # path('mark-sales-archived/', campaignleadshtmx.mark_sales_archived, name='mark-sales-archived' ),
    
    path('create-lead-note/', campaignleadshtmx.create_lead_note, name='create-lead-note' ),
    path('edit-lead/', campaignleadshtmx.edit_lead, name='edit-lead' ),
    path('add-campaign-category/', campaignleadshtmx.add_campaign_category, name='add-campaign-category' ),
    
    # path('test-whatsapp-message/', campaignleadshtmx.test_whatsapp_message, name='test-whatsapp-message' ),
    # path('template-editor/', campaignleadshtmx.template_editor, name='template-editor' ),
    # path('template-save/', campaignleadshtmx.template_save, name='template-save' ),
    
    path('campaign-lead-get-modal-content/', campaignleadshtmx.get_modal_content, name='campaign-lead-get-modal-content' ),
    path('campaign-lead-get-modal-content/<str:param1>/', campaignleadshtmx.get_modal_content, name='campaign-lead-get-modal-content' ),
    path('campaign-lead-get-modal-content/<str:param1>/<str:param2>/', campaignleadshtmx.get_modal_content, name='campaign-lead-get-modal-content' ),

    path('new-call/', campaignleadsviews.new_call, name='new-call' ),
    path('new-call/<int:lead_pk>/<int:call_count>/<int:max_call_count>/', campaignleadsviews.new_call, name='new-call' ),

    
    path('configuration/campaign-assign-auto-send-template/', campaignleadsviews.campaign_assign_auto_send_template_htmx, name='campaign-assign-auto-send-template'), 
    path('configuration/campaign-assign-color/', campaignleadsviews.campaign_assign_color_htmx, name='campaign-assign-color'), 
    path('configuration/refresh-campaign-configuration-row/', campaignleadsviews.refresh_campaign_configuration_row, name='refresh-campaign-configuration-row'), 
    
    path('configuration/profile-assign-campaign-category/', campaignleadsviews.profile_assign_campaign_category_htmx, name='profile-assign-campaign-category'), 
    path('configuration/campaign-assign-campaign-category/', campaignleadsviews.campaign_assign_campaign_category_htmx, name='campaign-assign-campaign-category'), 
    path('configuration/campaign-assign-whatsapp-business-account/', campaignleadsviews.campaign_assign_whatsapp_business_account_htmx, name='campaign-assign-whatsapp-business-account'), 
    path('configuration/campaign-assign-product_cost/', campaignleadsviews.campaign_assign_product_cost_htmx, name='campaign-assign-product_cost'), 
    path('get-contacts-for-campaign/', campaignleadshtmx.get_contacts_for_campaign, name='get-contacts-for-campaign'), 
    
]
