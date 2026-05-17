"""Serializers for the Notifications app."""
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'username', 'message', 'is_read',
            'created_at', 'application_id', 'job_title', 'candidate_name'
        ]
        read_only_fields = ['user', 'created_at', 'application_id', 'job_title', 'candidate_name']
