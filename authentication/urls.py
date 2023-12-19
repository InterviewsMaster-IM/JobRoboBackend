from django.urls import path
from . import views  # Ensure that this import line correctly points to your views

urlpatterns = [

    # URL pattern for starting the LinkedIn login process
    path('linkedin/login/', views.linkedin_login, name='linkedin_login'),

    # URL pattern for handling the callback from LinkedIn
    path('linkedin/callback/', views.linkedin_callback, name='linkedin_callback'),

]
