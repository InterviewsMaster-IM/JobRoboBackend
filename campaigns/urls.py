# campaigns/urls.py
from django.urls import path
from .views import create_campaign, update_campaign

urlpatterns = [
    # ... other url patterns
    path('create/,'create_campaign,name='create_campaign'),
    path('update_campaign/', update_campaign, name='update_campaign'),
]