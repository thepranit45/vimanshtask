"""Views for the Notifications app (API)."""
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    GET /api/notifications/
    Returns notifications for the authenticated user.
    Supports: ?is_read=true/false
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user)
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            qs = qs.filter(is_read=(is_read.lower() == 'true'))
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        unread_count = queryset.filter(is_read=False).count()
        return Response({
            'total': queryset.count(),
            'unread_count': unread_count,
            'notifications': serializer.data
        })


class NotificationMarkReadView(APIView):
    """
    PATCH /api/notifications/{id}/read/   - Mark as read
    PATCH /api/notifications/{id}/unread/ - Mark as unread
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, action):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        if action == 'read':
            notification.is_read = True
        elif action == 'unread':
            notification.is_read = False
        else:
            return Response({'error': 'Invalid action. Use read or unread.'}, status=status.HTTP_400_BAD_REQUEST)
        notification.save()
        return Response(NotificationSerializer(notification).data)


class NotificationMarkAllReadView(APIView):
    """PATCH /api/notifications/mark-all-read/ - Mark all as read"""
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': f'{count} notifications marked as read.'})
