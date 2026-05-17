"""Frontend URL routes for the web UI."""
from django.urls import path
from . import frontend_views

urlpatterns = [
    # Auth
    path('', frontend_views.dashboard_view, name='dashboard'),
    path('login/', frontend_views.login_view, name='login'),
    path('register/', frontend_views.register_view, name='register'),
    path('logout/', frontend_views.logout_view, name='logout'),

    # Recruiter portal
    path('jobs/', frontend_views.job_list_view, name='job-list'),
    path('jobs/<int:pk>/', frontend_views.job_detail_view, name='job-detail-ui'),
    path('candidates/', frontend_views.candidate_list_view, name='candidate-list'),
    path('notifications/', frontend_views.notification_list_view, name='notification-list-ui'),

    # Candidate portal
    path('candidate/register/', frontend_views.candidate_register_view, name='candidate-register'),
    path('candidate/login/', frontend_views.login_view, name='candidate-login'),
    path('candidate/dashboard/', frontend_views.candidate_portal_dashboard, name='candidate-portal-dashboard'),
    path('candidate/jobs/', frontend_views.candidate_portal_jobs, name='candidate-portal-jobs'),
    path('candidate/my-applications/', frontend_views.candidate_portal_my_applications, name='candidate-portal-applications'),

    # Public apply
    path('apply/<int:job_id>/', frontend_views.apply_public_view, name='apply-public'),
    path('apply/<int:job_id>/success/', frontend_views.apply_success_view, name='apply-success'),
]
