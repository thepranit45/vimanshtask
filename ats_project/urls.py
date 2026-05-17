"""ATS Project URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # API Routes
    path('api/auth/', include('accounts.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/candidates/', include('candidates.urls')),
    path('api/notifications/', include('notifications.urls')),
    # Frontend Routes
    path('', include('accounts.frontend_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
