from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect, name='dispatch')
class NotificationsView(APIView):
    """
    API endpoint for retrieving user notifications
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Get notifications for the current user
            notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
            
            # Prepare the response data
            notifications_data = []
            for notification in notifications:
                notifications_data.append({
                    'id': notification.id,
                    'title': notification.title,
                    'content': notification.content,
                    'created_at': notification.created_at,
                    'read': notification.read,
                    'type': notification.type,
                    'challenge_id': notification.challenge.id if notification.challenge else None,
                    'challenge_name': notification.challenge.name if notification.challenge else None,
                    'status': notification.status
                })
            
            return Response(notifications_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve notifications: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class MarkNotificationReadView(APIView):
    """
    API endpoint for marking a notification as read
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, notification_id):
        try:
            # Get the notification
            notification = Notification.objects.get(id=notification_id, user=request.user)
            
            # Mark as read
            notification.read = True
            notification.save()
            
            return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to mark notification as read: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class MarkAllNotificationsReadView(APIView):
    """
    API endpoint for marking all notifications as read
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Get all unread notifications for the user
            notifications = Notification.objects.filter(user=request.user, read=False)
            
            # Mark all as read
            for notification in notifications:
                notification.read = True
                notification.save()
            
            return Response({'message': 'All notifications marked as read'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to mark all notifications as read: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UnreadNotificationsCountView(APIView):
    """
    API endpoint for getting the count of unread notifications
    """
    def get(self, request):
        try:
            # Return 0 for unauthenticated users
            if not request.user.is_authenticated:
                return Response({'count': 0}, status=status.HTTP_200_OK)
            
            # Count unread notifications for authenticated users
            count = Notification.objects.filter(user=request.user, read=False).count()
            
            return Response({'count': count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to get unread notifications count: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
