"""Admin registration for Jobs app."""
from django.contrib import admin
from .models import Job, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'posted_by', 'application_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['required_skills']
    readonly_fields = ['created_at', 'updated_at']

    def application_count(self, obj):
        return obj.applications.count()
    application_count.short_description = 'Applications'
