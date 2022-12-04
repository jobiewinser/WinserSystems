"""jobiewebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
import analytics.views as analyticviews
import analytics.htmx as analyticshtmx
urlpatterns = [
    path('analytics-overview/', analyticviews.AnalyticsOverviewView.as_view(), name='analytics-overview' ),

    path('refresh-analytics/', analyticviews.refresh_analytics, name='refresh-analytics'),
    # path('get-leads-to-sales/', analyticshtmx.get_leads_to_sales, name='get-leads-to-sales' ),
    # path('get-leads-to-bookings/', analyticshtmx.get_leads_to_bookings, name='get-leads-to-bookings' ),
    path('get-leads-to-bookings-and-sales/', analyticshtmx.get_leads_to_bookings_and_sales, name='get-leads-to-bookings-and-sales' ),
    path('get-current-call-count-distribution/', analyticshtmx.get_current_call_count_distribution, name='get-current-call-count-distribution' ),
    
    path('get-calls-today/', analyticshtmx.get_calls_today, name='get-calls-today' ),
    path('get-sales-today/', analyticshtmx.get_sales_today, name='get-sales-today' ),
    path('get-calls-made-per-day/', analyticshtmx.get_calls_made_per_day, name='get-calls-made-per-day' ),
    
    path('get-pipeline/', analyticshtmx.get_pipeline, name='get-pipeline' ),
    
    
    # path('get-base-analytics/', analyticshtmx.get_base_analytics, name='get-base-analytics' ),
]
