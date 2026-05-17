"""Models for the Notifications app."""
from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """Notification created when a candidate applies for a job."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Reference to the application that triggered this notification
    application_id = models.IntegerField(null=True, blank=True)
    job_title = models.CharField(max_length=255, blank=True, default='')
    candidate_name = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        status = "Read" if self.is_read else "Unread"
        return f"[{status}] {self.user.username}: {self.message[:50]}"

    class Meta:
        ordering = ['-created_at']
