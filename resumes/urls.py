from django.urls import path
from .views import resume_upload, start_parse_resume_task, check_parse_resume_task_status

urlpatterns = [
    path('upload/', resume_upload, name='file-upload'),
    path('start-task/', start_parse_resume_task, name='start-parse-resume-task'),
    path('check-task/<str:task_id>/', check_parse_resume_task_status, name='check-parse-resume-task-status'),
]