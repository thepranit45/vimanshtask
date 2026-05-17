"""Admin registration for Candidates app."""
from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'job', 'score', 'status', 'applied_at']
    list_filter = ['status', 'applied_at', 'job']
    search_fields = ['name', 'email']
    readonly_fields = ['score', 'summary', 'applied_at']
    filter_horizontal = ['skills']
    ordering = ['-score']
