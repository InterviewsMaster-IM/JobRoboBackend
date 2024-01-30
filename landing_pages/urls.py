from django.urls import path, re_path
from . import views

urlpatterns = [
    # Catch-all for React routing
    re_path(r'^(?:.*)/?$', views.home),
]
