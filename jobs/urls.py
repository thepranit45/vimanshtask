"""URL routes for the Jobs API."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListCreateView.as_view(), name='job-list-create'),
    path('skills/', views.SkillListCreateView.as_view(), name='skill-list-create'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('<int:pk>/candidates/', views.JobCandidatesView.as_view(), name='job-candidates'),
    path('<int:job_id>/apply/', __import__('candidates.views', fromlist=['ApplyForJobView']).ApplyForJobView.as_view(), name='apply-for-job'),
]
