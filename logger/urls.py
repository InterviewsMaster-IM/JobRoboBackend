from django.urls import path
from .views import log_entries

urlpatterns = [
    path('', log_entries, name='log_entries'),
]
