# profiles/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Existing paths
    path('skills/', skill_list_create_view, name='skill-list-create'),
    path('skills/<int:pk>/', skill_detail_view, name='skill-detail'),

    # WorkExperience paths
    path('work-experience/', work_experience_list_create_view,
         name='work-experience-list-create'),
    path('work-experience/<int:pk>/', work_experience_detail_view,
         name='work-experience-detail'),

    # Education paths
    path('education/', education_list_create_view, name='education-list-create'),
    path('education/<int:pk>/', education_detail_view, name='education-detail'),

    # PersonalInfo path
    path('personal-info/', personal_info_view, name='personal-info'),
]
