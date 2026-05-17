"""Models for the Jobs app."""
from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    """Represents a skill tag (e.g. Python, Django, React)."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Job(models.Model):
    """A job posting with required skills."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('paused', 'Paused'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    required_skills = models.ManyToManyField(Skill, related_name='jobs', blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        ordering = ['-created_at']
