from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from campaign_leads.models import Call, Campaign, Campaignlead, CampaignCategory, Sale, Booking
from core.models import Site
from dateutil import relativedelta
from django.contrib.auth.models import User
from core.templatetags.core_tags import short_month_name
from django.db.models import Sum
from django.db.models import Q, Count
from analytics.views import get_minimum_site_subscription_level_from_site_qs

def check_if_start_date_allowed_and_replace(start_date, site_qs, lead_qs=None, sale_qs=None, booking_qs=None):
    # if not site_qs and lead_qs:
    #     site_qs = Site.objects.filter(campaign__campaignlead__in=lead_qs).exclude(active=False)
    # if not site_qs and sale_qs:
    #     site_qs = Site.objects.filter(campaign__campaignlead__sale__in=sale_qs).exclude(active=False)
    # if not site_qs and booking_qs:
    #     site_qs = Site.objects.filter(campaign__campaignlead__booking__in=booking_qs).exclude(active=False)
    subscription = get_minimum_site_subscription_level_from_site_qs(site_qs)
    earliest_site = site_qs.order_by('created').first()
    if subscription.analytics_seconds: 
        minimum_datetime_allowed = datetime.now() - relativedelta.relativedelta(days = round(subscription.analytics_seconds/86400))
    elif earliest_site:
        minimum_datetime_allowed = earliest_site.created
    else:
        return datetime.now()
        
        
    if start_date > minimum_datetime_allowed and start_date > earliest_site.created: #if queried date is all good
        return start_date
    if start_date > earliest_site.created: #if queried date is correctly after earliest site in query
        return datetime.strptime(str(minimum_datetime_allowed)[0:10], '%Y-%m-%d')
    if start_date > minimum_datetime_allowed: #if queried date is correctly after the allowed date by subscription
        return datetime.strptime(str(earliest_site.created)[0:10], '%Y-%m-%d')


    if earliest_site.created > minimum_datetime_allowed:        
        return datetime.strptime(str(earliest_site.created)[0:10], '%Y-%m-%d')
    else:
        return datetime.strptime(str(minimum_datetime_allowed)[0:10], '%Y-%m-%d')
    
def get_leads_per_day_between_dates_with_timeframe_differences(start_date, end_date, timeframe=relativedelta.relativedelta(days=1), campaigns=[], campaign_categorys=[], sites=[]):
    qs = Campaignlead.objects.filter(created__gte=start_date, created__lt=end_date + timeframe)
    if qs.exists():
        start_date = check_if_start_date_allowed_and_replace(start_date, sites, lead_qs=qs)
        if campaigns:
            qs = qs.filter(campaign__in=campaigns)
        elif campaign_categorys:
            qs = qs.filter(campaign__campaign_category__in=campaign_categorys)
        elif sites:
            qs = qs.filter(campaign__site__in=sites)   
        if qs.exists(): 
            index_date = start_date
            time_label_set = []
            data_set = []
            while index_date < end_date + timeframe:
                index_qs = qs.filter(created__gte=index_date, created__lt=index_date + timeframe)
                leads = index_qs.count()
                data_set.append({
                    'leads':leads,
                })
                time_label_set.append(f"{index_date}")
                index_date = index_date + timeframe
            return data_set, time_label_set, start_date  
    return [], [], start_date  

def get_sales_per_day_between_dates_with_timeframe_differences(start_date, end_date, timeframe=relativedelta.relativedelta(days=1), campaigns=[], campaign_categorys=[], sites=[]):
    qs = Sale.objects.filter(datetime__gte=start_date, datetime__lt=end_date + timeframe).exclude(archived=True)
    if qs.exists():
        start_date = check_if_start_date_allowed_and_replace(start_date, sites, sale_qs=qs)
        if campaigns:
            qs = qs.filter(lead__campaign__in=campaigns)
        elif campaign_categorys:
            qs = qs.filter(lead__campaign__campaign_category__in=campaign_categorys)
        elif sites:
            qs = qs.filter(lead__campaign__site__in=sites)
        if qs.exists():  
            unique_user_list = User.objects.filter(is_active=True, pk__in=set(qs.values_list('user', flat=True).distinct()))       
            time_label_set = []
            data_set = {
                "Deactivated Users":{'color':"135,135,135", 'data':[]},
                "Deleted Users":{'color':"0,0,0", 'data':[]},
            }
            index_date = start_date
            deactivated_user_entry_found = False
            deleted_user_entry_found = False
            for user in unique_user_list:
                data_set[user.profile.name] = {'color':user.profile.color, 'data':[]}
            
            while index_date < end_date + timeframe:
                time_label_set.append(f"{index_date}")
                index_qs = qs.filter(datetime__gte=index_date, datetime__lt=index_date + timeframe)
                for user in unique_user_list:
                    data_set[user.profile.name]['data'].append(index_qs.filter(user=user).count())
                deactivated_user_count = index_qs.filter(user__is_active=False).count()
                if deactivated_user_count:
                    deactivated_user_entry_found = True
                deleted_user_count = index_qs.filter(user=None).count()
                if deleted_user_count:
                    deleted_user_entry_found = True
                data_set["Deactivated Users"]['data'].append(deactivated_user_count)
                data_set["Deleted Users"]['data'].append(deleted_user_count)
                
                index_date = index_date + timeframe
            if not deactivated_user_entry_found:
                data_set.pop('Deactivated Users')
            if not deleted_user_entry_found:
                data_set.pop('Deleted Users')
            return data_set, time_label_set, start_date  
    return [], [], start_date  

def get_bookings_per_day_between_dates_with_timeframe_differences(start_date, end_date, timeframe=relativedelta.relativedelta(days=1), campaigns=[], campaign_categorys=[], sites=[]):
    qs = Booking.objects.filter(created__gte=start_date, created__lt=end_date + timeframe).exclude(archived=True)
    if qs.exists():
        start_date = check_if_start_date_allowed_and_replace(start_date, sites, booking_qs=qs)
        if campaigns:
            qs = qs.filter(lead__campaign__in=campaigns)
        elif campaign_categorys:
            qs = qs.filter(lead__campaign__campaign_category__in=campaign_categorys)
        elif sites:
            qs = qs.filter(lead__campaign__site__in=sites)
        if qs.exists():
            unique_user_list = User.objects.filter(is_active=True, pk__in=set(qs.values_list('user', flat=True).distinct())) 
            time_label_set = []
            data_set = {
                "Deactivated Users":{'color':"135,135,135", 'data':[]},
                "Deleted Users":{'color':"0,0,0", 'data':[]},
            }
            index_date = start_date
            deactivated_user_entry_found = False
            deleted_user_entry_found = False
            for user in unique_user_list:
                data_set[user.profile.name] = {'color':user.profile.color, 'data':[]}
            
            while index_date < end_date + timeframe:
                time_label_set.append(f"{index_date}")
                index_qs = qs.filter(created__gte=index_date, created__lt=index_date + timeframe)
                for user in unique_user_list:
                    data_set[user.profile.name]['data'].append(index_qs.filter(user=user).count())
                deactivated_user_count = index_qs.filter(user__is_active=False).count()
                if deactivated_user_count:
                    deactivated_user_entry_found = True
                deleted_user_count = index_qs.filter(user=None).count()
                if deleted_user_count:
                    deleted_user_entry_found = True
                data_set["Deactivated Users"]['data'].append(deactivated_user_count)
                data_set["Deleted Users"]['data'].append(deleted_user_count)
                
                index_date = index_date + timeframe
            if not deactivated_user_entry_found:
                data_set.pop('Deactivated Users')
            if not deleted_user_entry_found:
                data_set.pop('Deleted Users')
            # index_date = start_date
            # time_label_set = []
            # data_set = []
            # while index_date < end_date + timeframe:
            #     index_qs = qs.filter(created__gte=index_date, created__lt=index_date + timeframe).count()
                
            #     data_set.append({
            #         'bookings':index_qs,
            #     })
            #     time_label_set.append(f"{index_date}")
            #     index_date = index_date + timeframe
            return data_set, time_label_set, start_date  
    return [], [], start_date  
    
def get_calls_made_per_day_between_dates(start_date, end_date, user, timeframe=relativedelta.relativedelta(days=1), campaigns=[], campaign_categorys=[], sites=[], get_user_totals=False):
    qs = Call.objects.filter(datetime__gte=start_date, datetime__lt=end_date + timeframe)
    if qs.exists():
        if campaigns:
            qs = qs.filter(lead__campaign__in=campaigns)
        elif campaign_categorys:
            qs = qs.filter(lead__campaign__campaign_category__in=campaign_categorys)
        elif sites:
            qs = qs.filter(lead__campaign__site__in=sites)
        if qs.exists():
            unique_user_list = User.objects.filter(is_active=True, pk__in=set(qs.values_list('user', flat=True).distinct())) 
            time_label_set = []
            data_set = {
                "Deactivated Users":{'color':"135,135,135", 'data':[]},
                "Deleted Users":{'color':"0,0,0", 'data':[]},
            }
            index_date = start_date
            deactivated_user_entry_found = False
            deleted_user_entry_found = False
            for user in unique_user_list:
                data_set[user.profile.name] = {'color':user.profile.color, 'data':[]}
            
            while index_date < end_date + timeframe:
                time_label_set.append(f"{index_date}")
                index_qs = qs.filter(datetime__gte=index_date, datetime__lt=index_date + timeframe)
                for user in unique_user_list:
                    data_set[user.profile.name]['data'].append(index_qs.filter(user=user).count())
                deactivated_user_count = index_qs.filter(user__is_active=False).count()
                if deactivated_user_count:
                    deactivated_user_entry_found = True
                deleted_user_count = index_qs.filter(user=None).count()
                if deleted_user_count:
                    deleted_user_entry_found = True
                data_set["Deactivated Users"]['data'].append(deactivated_user_count)
                data_set["Deleted Users"]['data'].append(deleted_user_count)
                
                index_date = index_date + timeframe
            if not deactivated_user_entry_found:
                data_set.pop('Deactivated Users')
            if not deleted_user_entry_found:
                data_set.pop('Deleted Users')
            return data_set, time_label_set, start_date
    return [], [], start_date  

def get_calls_today_dataset(campaigns=[], campaign_categorys=[], sites=[]):
    data_set = {}
    qs = Call.objects.filter(datetime__gte= datetime.now().replace(hour=0,minute=0,second=0,microsecond=0))
    if campaigns:
        qs = qs.filter(lead__campaign__in=campaigns)
    elif campaign_categorys:
        qs = qs.filter(lead__campaign__campaign_category__in=campaign_categorys)
    elif sites:
        qs = qs.filter(lead__campaign__site__in=sites)
    unique_users = list(qs.order_by('user').distinct('user').values_list('user', flat=True))
    if unique_users:
        for user_pk in unique_users:
            if user_pk:
                user = User.objects.get(pk=user_pk)
                data_set[user.profile.pk] = {
                    'name':user.profile.name,
                    'color':user.profile.color,
                    'data':qs.filter(user=user).count(),
                }
    deactivated_user_count = qs.filter(user__is_active=False).count()
    if deactivated_user_count:
        data_set['0'] = {
            'name':"Deactivated Users",
            'color':"135,135,135",
            'data':deactivated_user_count,
        }
    deleted_user_count = qs.filter(user=None).count()
    if deleted_user_count:
        data_set['0'] = {
            'name':"Deleted Users",
            'color':"0,0,0",
            'data':deleted_user_count,
        }
    return data_set, qs

def get_sales_today_dataset(campaigns=[], campaign_categorys=[], sites=[]):
    data_set = {}
    qs = Sale.objects.filter(datetime__gte=datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).exclude(archived=True)
    if campaigns:
        qs = qs.filter(lead__campaign__in=campaigns)
    elif campaign_categorys:
        qs = qs.filter(lead__campaign__campaign_category__in=campaign_categorys)
    elif sites:
        qs = qs.filter(lead__campaign__site__in=sites)
    unique_users = list(qs.order_by('user').distinct('user').values_list('user', flat=True))
    if unique_users:
        for user_pk in unique_users:
            if user_pk:
                user = User.objects.get(pk=user_pk)
                data_set[user.profile.pk] = {
                    'name':user.profile.name,
                    'color':user.profile.color,
                    'data':qs.filter(user=user).count(),
                }
    deactivated_user_count = qs.filter(user__is_active=False).count()
    if deactivated_user_count:
        data_set['0'] = {
            'name':"Deactivated Users",
            'color':"135,135,135",
            'data':deactivated_user_count,
        }
    deleted_user_count = qs.filter(user=None).count()
    if deleted_user_count:
        data_set['0'] = {
            'name':"Deleted Users",
            'color':"0,0,0",
            'data':deleted_user_count,
        }
    return data_set, qs
    
@login_required
def get_leads_per_day(request):
    context = {}
    campaign_pks = request.GET.getlist('campaign_pks', [])
    campaign_category_pks = request.GET.getlist('campaign_category_pks', [])
    campaigns = None
    campaign_categorys = None
    sites = []
    if campaign_pks:
        campaigns = Campaign.objects.filter(pk__in=campaign_pks)
        # sites = Site.objects.filter(campaign__in=campaigns).exclude(active=False)
    elif campaign_category_pks:
        campaign_categorys = CampaignCategory.objects.filter(pk__in=campaign_category_pks)
    #     sites = Site.objects.filter(campaigncategory__in=campaign_categorys).exclude(active=False)
    # else:
    site_pks = request.GET.getlist('site_pks', request.user.profile.active_sites_allowed)
    sites = request.user.profile.active_sites_allowed.filter(pk__in=site_pks)

    start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d') + relativedelta.relativedelta(days=1) 

    data_set, time_label_set, start_date = get_leads_per_day_between_dates_with_timeframe_differences(start_date, end_date, campaigns=campaigns, campaign_categorys=campaign_categorys, sites=sites)
        
    context['data_set'] = data_set
    context['time_label_set'] = time_label_set
    context['start_date'] = start_date
    context['end_date'] = end_date
    if request.GET.get('graph_type', 'off') == 'on':
        context['graph_type'] = 'line'
    else:
        context['graph_type'] = 'bar'
    context['minimum_site_subscription_level_in_query'] = get_minimum_site_subscription_level_from_site_qs(sites)
    return render(request, 'analytics/htmx/leads_per_day_data.html', context)
    
@login_required
def get_bookings_per_day(request):
    context = {}
    campaign_pks = request.GET.getlist('campaign_pks', [])
    campaign_category_pks = request.GET.getlist('campaign_category_pks', [])
    campaigns = None
    campaign_categorys = None
    sites = []
    if campaign_pks:
        campaigns = Campaign.objects.filter(pk__in=campaign_pks)
        # sites = Site.objects.filter(campaign__in=campaigns).exclude(active=False)
    elif campaign_category_pks:
        campaign_categorys = CampaignCategory.objects.filter(pk__in=campaign_category_pks)
    #     sites = Site.objects.filter(campaigncategory__in=campaign_categorys).exclude(active=False)
    # else:
    site_pks = request.GET.getlist('site_pks', request.user.profile.active_sites_allowed)
    sites = request.user.profile.active_sites_allowed.filter(pk__in=site_pks)

    start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d') + relativedelta.relativedelta(days=1) 

    data_set, time_label_set, start_date = get_bookings_per_day_between_dates_with_timeframe_differences(start_date, end_date, campaigns=campaigns, campaign_categorys=campaign_categorys, sites=sites)
        
    context['data_set'] = data_set
    context['time_label_set'] = time_label_set
    context['start_date'] = start_date
    context['end_date'] = end_date
    if request.GET.get('graph_type', 'off') == 'on':
        context['graph_type'] = 'line'
    else:
        context['graph_type'] = 'bar'
    context['minimum_site_subscription_level_in_query'] = get_minimum_site_subscription_level_from_site_qs(sites)
    return render(request, 'analytics/htmx/bookings_per_day_data.html', context)
    
@login_required
def get_sales_per_day(request):
    context = {}
    campaign_pks = request.GET.getlist('campaign_pks', [])
    campaign_category_pks = request.GET.getlist('campaign_category_pks', [])
    campaigns = None
    campaign_categorys = None
    sites = []
    if campaign_pks:
        campaigns = Campaign.objects.filter(pk__in=campaign_pks)
        # sites = Site.objects.filter(campaign__in=campaigns).exclude(active=False)
    elif campaign_category_pks:
        campaign_categorys = CampaignCategory.objects.filter(pk__in=campaign_category_pks)
    #     sites = Site.objects.filter(campaigncategory__in=campaign_categorys).exclude(active=False)
    # else:
    site_pks = request.GET.getlist('site_pks', request.user.profile.active_sites_allowed)
    sites = request.user.profile.active_sites_allowed.filter(pk__in=site_pks)

    start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d') + relativedelta.relativedelta(days=1) 

    data_set, time_label_set, start_date = get_sales_per_day_between_dates_with_timeframe_differences(start_date, end_date, campaigns=campaigns, campaign_categorys=campaign_categorys, sites=sites)
        
    context['data_set'] = data_set
    context['time_label_set'] = time_label_set
    context['start_date'] = start_date
    context['end_date'] = end_date
    if request.GET.get('graph_type', 'off') == 'on':
        context['graph_type'] = 'line'
    else:
        context['graph_type'] = 'bar'
    context['minimum_site_subscription_level_in_query'] = get_minimum_site_subscription_level_from_site_qs(sites)
    return render(request, 'analytics/htmx/sales_per_day_data.html', context)
    
@login_required()
def get_calls_today(request):
    context = {}
    campaign_pks = request.GET.getlist('campaign_pks', [])
    campaign_category_pks = request.GET.getlist('campaign_category_pks', [])
    campaigns = None
    campaign_categorys = None
    sites = []
    if campaign_pks:
        campaigns = Campaign.objects.filter(pk__in=campaign_pks)
        # sites = Site.objects.filter(campaign__in=campaigns).exclude(active=False)
    elif campaign_category_pks:
        campaign_categorys = CampaignCategory.objects.filter(pk__in=campaign_category_pks)
    #     sites = Site.objects.filter(campaigncategory__in=campaign_categorys).exclude(active=False)
    # else:
    site_pks = request.GET.getlist('site_pks', request.user.profile.active_sites_allowed)
    sites = request.user.profile.active_sites_allowed.filter(pk__in=site_pks)

    data_set, raw_qs = get_calls_today_dataset(campaigns=campaigns, campaign_categorys=campaign_categorys, sites=sites)
        
    context['data_set'] = data_set
    context['raw_qs'] = raw_qs
    if request.GET.get('graph_type', 'off') == 'on':
        context['graph_type'] = 'polarArea'
    else:
        context['graph_type'] = 'doughnut'
    context['minimum_site_subscription_level_in_query'] = get_minimum_site_subscription_level_from_site_qs(sites)
    return render(request, 'analytics/htmx/calls_today_data.html', context)

@login_required()
def get_sales_today(request):
    context = {}
    campaign_pks = request.GET.getlist('campaign_pks', [])
    campaign_category_pks = request.GET.getlist('campaign_category_pks', [])
    campaigns = None
    campaign_categorys = None
    sites = []
    if campaign_pks:
        campaigns = Campaign.objects.filter(pk__in=campaign_pks)
        # sites = Site.objects.filter(campaign__in=campaigns).exclude(active=False)
    elif campaign_category_pks:
        campaign_categorys = CampaignCategory.objects.filter(pk__in=campaign_category_pks)
    #     sites = Site.objects.filter(campaigncategory__in=campaign_categorys).exclude(active=False)
    # else:
    site_pks = request.GET.getlist('site_pks', request.user.profile.active_sites_allowed)
    sites = request.user.profile.active_sites_allowed.filter(pk__in=site_pks)
    
    data_set, raw_qs = get_sales_today_dataset(campaigns=campaigns, campaign_categorys=campaign_categorys, sites=sites)
        
    context['data_set'] = data_set
    context['raw_qs'] = raw_qs
    if request.GET.get('graph_type', 'off') == 'on':
        context['graph_type'] = 'polarArea'
    else:
        context['graph_type'] = 'doughnut'
    context['minimum_site_subscription_level_in_query'] = get_minimum_site_subscription_level_from_site_qs(sites)
    return render(request, 'analytics/htmx/sales_today_data.html', context)
    
@login_required
def get_calls_made_per_day(request):
    context = {}
    campaign_pks = request.GET.getlist('campaign_pks', [])
    campaign_category_pks = request.GET.getlist('campaign_category_pks', [])
    campaigns = None
    campaign_categorys = None
    sites = []
    if campaign_pks:
        campaigns = Campaign.objects.filter(pk__in=campaign_pks)
        # sites = Site.objects.filter(campaign__in=campaigns).exclude(active=False)
    elif campaign_category_pks:
        campaign_categorys = CampaignCategory.objects.filter(pk__in=campaign_category_pks)
    #     sites = Site.objects.filter(campaigncategory__in=campaign_categorys).exclude(active=False)
    # else:
    site_pks = request.GET.getlist('site_pks', request.user.profile.active_sites_allowed)
    sites = request.user.profile.active_sites_allowed.filter(pk__in=site_pks)

    start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d') + relativedelta.relativedelta(days=1) 
    
    data_set, time_label_set, start_date = get_calls_made_per_day_between_dates(start_date, end_date, request.user, campaigns=campaigns, campaign_categorys=campaign_categorys, sites=sites)
        
    context['data_set'] = data_set
    context['time_label_set'] = time_label_set
    context['start_date'] = start_date
    context['end_date'] = end_date
    if request.GET.get('graph_type', 'off') == 'on':
        context['graph_type'] = 'line'
    else:
        context['graph_type'] = 'bar'
    context['minimum_site_subscription_level_in_query'] = get_minimum_site_subscription_level_from_site_qs(sites)
    return render(request, 'analytics/htmx/calls_made_per_day_data.html', context)

@login_required
def get_current_call_count_distribution(request):
    context = {}
    campaign_pks = request.GET.getlist('campaign_pks', [])
    campaign_category_pks = request.GET.getlist('campaign_category_pks', [])
    campaigns = None
    campaign_categorys = None
    sites = []
    if campaign_pks:
        campaigns = Campaign.objects.filter(pk__in=campaign_pks)
        # sites = Site.objects.filter(campaign__in=campaigns).exclude(active=False)
    elif campaign_category_pks:
        campaign_categorys = CampaignCategory.objects.filter(pk__in=campaign_category_pks)
    #     sites = Site.objects.filter(campaigncategory__in=campaign_categorys).exclude(active=False)
    # else:
    site_pks = request.GET.getlist('site_pks', request.user.profile.active_sites_allowed)
    sites = request.user.profile.active_sites_allowed.filter(pk__in=site_pks)
    
    non_time_filtered_live_opportunities = Campaignlead.objects.filter(booking = None, archived = False).exclude(sale__archived=False).annotate(calls=Count('call'))
    
    if campaigns:
        non_time_filtered_opportunities = non_time_filtered_live_opportunities.filter(campaign__site__company=request.user.profile.company, campaign__in=campaigns, campaign__site__in=request.user.profile.active_sites_allowed)
    if campaign_categorys:
        non_time_filtered_opportunities = non_time_filtered_live_opportunities.filter(campaign__campaign_category__site__company=request.user.profile.company, campaign__campaign_category__in=campaign_categorys, campaign__campaign_category__site__in=request.user.profile.active_sites_allowed)
    elif sites:
        non_time_filtered_opportunities = non_time_filtered_live_opportunities.filter(campaign__site__company=request.user.profile.company, campaign__site__in=sites).filter(campaign__site__in=request.user.profile.active_sites_allowed)
    else:
        non_time_filtered_opportunities = non_time_filtered_live_opportunities.filter(campaign__site__company=request.user.profile.company, campaign__site__in=request.user.profile.active_sites_allowed)


    call_counts_tuples = []
    index = 0
    if non_time_filtered_opportunities.filter(calls__gte=index):
        while non_time_filtered_opportunities.filter(calls__gte=index):
            if non_time_filtered_opportunities.exclude(calls=index).count():
                queryset_percentage_portion = (non_time_filtered_opportunities.filter(calls=index).count() / non_time_filtered_opportunities.count())*100
            elif non_time_filtered_opportunities.filter(calls=index).count():
                queryset_percentage_portion = 100
            else:
                queryset_percentage_portion = 0
            call_counts_tuples.append((index, non_time_filtered_opportunities.filter(calls=index).count(), non_time_filtered_live_opportunities.filter(calls=index).aggregate(Sum('campaign__product_cost')), queryset_percentage_portion))
            index = index + 1
    else:
        pass
    context['call_counts_tuples'] = call_counts_tuples
    context['minimum_site_subscription_level_in_query'] = get_minimum_site_subscription_level_from_site_qs(sites)
    return render(request, 'analytics/htmx/current_call_count_distribution_data.html', context)
@login_required
def get_pipeline(request):
    context = {}
    campaign_pks = request.GET.getlist('campaign_pks', [])
    campaign_category_pks = request.GET.getlist('campaign_category_pks', [])
    campaigns = None
    campaign_categorys = None
    sites = []
    if campaign_pks:
        campaigns = Campaign.objects.filter(pk__in=campaign_pks)
        # sites = Site.objects.filter(campaign__in=campaigns).exclude(active=False)
    elif campaign_category_pks:
        campaign_categorys = CampaignCategory.objects.filter(pk__in=campaign_category_pks)
    #     sites = Site.objects.filter(campaigncategory__in=campaign_categorys).exclude(active=False)
    # else:
    site_pks = request.GET.getlist('site_pks', request.user.profile.active_sites_allowed)
    sites = request.user.profile.active_sites_allowed.filter(pk__in=site_pks)

    start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')

    start_date = check_if_start_date_allowed_and_replace(start_date, site_qs=sites)

    end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d') + relativedelta.relativedelta(days=1)
            
    context['start_date'] = start_date
    context['end_date'] = end_date
    # if not request.user.profile.company.check_if_allowed_to_get_analytics(start_date):
    #     start_date = datetime.now() - timedelta(days=7)
    end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d') + relativedelta.relativedelta(days=1)   
    if campaigns:
        opportunities = Campaignlead.objects.filter(campaign__site__company=request.user.profile.company, campaign__in=campaigns, created__gte=start_date, created__lt=end_date, campaign__site__in=request.user.profile.active_sites_allowed).annotate(calls=Count('call'))
    if campaign_categorys:
        opportunities = Campaignlead.objects.filter(campaign__campaign_category__site__company=request.user.profile.company, campaign__campaign_category__in=campaign_categorys, created__gte=start_date, created__lt=end_date, campaign__campaign_category__site__in=request.user.profile.active_sites_allowed).annotate(calls=Count('call'))
    elif sites:
        opportunities = Campaignlead.objects.filter(campaign__site__company=request.user.profile.company, campaign__site__in=sites, created__gte=start_date, created__lt=end_date).filter(campaign__site__in=request.user.profile.active_sites_allowed).annotate(calls=Count('call'))
    else:
        opportunities = Campaignlead.objects.filter(campaign__site__company=request.user.profile.company, created__gte=start_date, created__lt=end_date, campaign__site__in=request.user.profile.active_sites_allowed).annotate(calls=Count('call'))

    live_opportunities = opportunities.exclude(archived=True).exclude(sale__archived=False)
    sold_opportunities = opportunities.filter(sale__archived=False, booking__archived=False)
    booked_opportunities = opportunities.filter(booking__archived=False)
    lost_opportunities = opportunities.filter(archived=True).exclude(sale__archived=False)

    context['opportunities'] = opportunities.count()
    context['live_opportunities'] = live_opportunities.count()
    context['sold_opportunities'] = sold_opportunities.count()
    context['booked_opportunities'] = booked_opportunities.count()
    context['lost_opportunities'] = lost_opportunities.count()
    
    if live_opportunities:
        context['live_value'] = float(live_opportunities.aggregate(Sum('campaign__product_cost')).get('campaign__product_cost__sum', 0))
    else:
        context['live_value'] = 0

    if sold_opportunities:
        context['sold_value'] = float(sold_opportunities.aggregate(Sum('campaign__product_cost')).get('campaign__product_cost__sum', 0))
    else:
        context['sold_value'] = 0

    if booked_opportunities:
        context['booked_value'] = float(booked_opportunities.aggregate(Sum('campaign__product_cost')).get('campaign__product_cost__sum', 0))
    else:
        context['booked_value'] = 0

    if lost_opportunities:
        context['lost_value'] = float(lost_opportunities.aggregate(Sum('campaign__product_cost')).get('campaign__product_cost__sum', 0))
    else:
        context['lost_value'] = 0

    if opportunities:
        context['opportunities_value'] = float(opportunities.aggregate(Sum('campaign__product_cost')).get('campaign__product_cost__sum', 0))
    else:
        context['opportunities_value'] = 0

    if context['live_opportunities'] or context['lost_opportunities']:
        context['booked_rate'] = (context['booked_opportunities'] / context['opportunities']) * 100
    elif context['live_opportunities']:
        context['booked_rate'] = 100
    else:
        context['booked_rate'] = 0

    if context['booked_opportunities']:
        context['sold_rate'] = (context['sold_opportunities'] / (context['booked_opportunities'])) * 100
    elif context['sold_opportunities']:
        context['sold_rate'] = 100
    else:
        context['sold_rate'] = 0
    context['start_date'] = start_date
    context['end_date'] = end_date
    context['minimum_site_subscription_level_in_query'] = get_minimum_site_subscription_level_from_site_qs(sites)
    return render(request, 'analytics/htmx/pipeline_data.html', context)
        