from django.urls import path
from .views import JobRoboListCreateView, JobBoardListView, JobTypeListView

urlpatterns = [
    path('jobrobos/', JobRoboListCreateView.as_view(), name='jobrobo-list-create'),
    path('jobboards/', JobBoardListView.as_view(), name='jobboard-list'),
    path('jobtypes/', JobTypeListView.as_view(), name='jobtype-list'),
]
