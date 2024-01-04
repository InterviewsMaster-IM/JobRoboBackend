# profiles/urls.py
from django.urls import path
from .views import add_other_details, get_other_details

urlpatterns = [
    path('other-details/add/', add_other_details, name='add-other-details'),
    path('other-details/', get_other_details, name='get-other-details'),
]
