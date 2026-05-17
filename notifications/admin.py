"""Admin registration for Notifications app."""
from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'candidate_name', 'job_title', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['message', 'candidate_name', 'job_title']
    readonly_fields = ['created_at']
