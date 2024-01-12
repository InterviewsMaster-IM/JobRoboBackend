# resumes/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', resume_upload, name='file-upload'),
    path('onboarding-details/', onboarding_details, name='onboarding_details'),
    path('coverletter/upload/', coverletter_upload, name='coverletter-upload'),
    path('start-task/', start_parse_resume_task,
         name='start-parse-resume-task'),
    path('check-task/<str:task_id>/', check_parse_resume_task_status,
         name='check-parse-resume-task-status'),
    path('qa/', resume_query_view, name='resume-query'),
    path('delete/<int:resume_id>/', delete_resume, name='delete-resume'),
    path('coverletter/delete/<int:coverletter_id>/',
         delete_coverletter, name='delete-coverletter'),

    path('uploads/', get_uploads, name='get-uploads'),
]
