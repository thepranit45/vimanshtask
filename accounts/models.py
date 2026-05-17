"""Models for the Accounts app - uses Django's built-in User."""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended profile for users."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate'),
    ], default='recruiter')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
