# credits/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('credit-plans/', views.CreditPlanListView.as_view(),
         name='credit-plan-list'),
    path('user-credits/', views.UserCreditsView.as_view(), name='user-credits'),
    path('credit-history/', views.CreditHistoryView.as_view(), name='credit-history'),
]
