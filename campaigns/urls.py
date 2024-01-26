from django.urls import path
from .views import create_campaign, update_campaign, get_user_campaigns, get_campaign_jobs_applied

urlpatterns = [
    # ... other url patterns
    path('create/', create_campaign, name='create_campaign'),
    path('update_campaign/', update_campaign, name='update_campaign'),
    path('user_campaigns/', get_user_campaigns, name='get_user_campaigns'),
    path('campaign_jobs/<int:campaign_id>/',
         get_campaign_jobs_applied, name='get_campaign_jobs_applied'),
]
