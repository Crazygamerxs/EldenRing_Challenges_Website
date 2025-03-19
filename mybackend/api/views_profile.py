# User Profile views have been removed as the User Profile feature is no longer needed

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserProfilePlaceholder(APIView):
    """
    Placeholder for removed user profile endpoints
    """
    def get(self, request, *args, **kwargs):
        return Response(
            {'error': 'User profile feature has been removed'},
            status=status.HTTP_404_NOT_FOUND
        )
