from django.urls import path
from .views import create_referral_code, validate_referral_code

urlpatterns = [
    path('create/', create_referral_code, name='create-referral-code'),
    path('validate/<str:code>/', validate_referral_code,
         name='validate-referral-code'),
]
