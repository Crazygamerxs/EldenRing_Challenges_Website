from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
import logging

logger = logging.getLogger('api')

class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Simple health check endpoint for monitoring"""
        try:
            # Test database connection
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            
            # Test cache connection if Redis is configured
            try:
                from django.core.cache import cache
                cache.set('health_check', 'ok', 30)
                cache_status = cache.get('health_check') == 'ok'
            except Exception:
                cache_status = False
            
            return Response({
                'status': 'healthy',
                'timestamp': timezone.now(),
                'version': '1.0.0',
                'database': 'connected',
                'cache': 'connected' if cache_status else 'disconnected'
            })
        except Exception as e:
            logger.error(f'Health check failed: {e}')
            return Response({
                'status': 'unhealthy',
                'timestamp': timezone.now(),
                'error': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
