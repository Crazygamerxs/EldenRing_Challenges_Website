from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Case, When, IntegerField, Q
from .models import User, Challenge, Submission, UserChallenge
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect, name='dispatch')
class LeaderboardChallengesView(APIView):
    """
    API endpoint for retrieving the leaderboard based on completed challenges
    """
    def get(self, request):
        try:
            # Get all users with the most completed challenges and their points
            users_with_challenges = User.objects.annotate(
                challenges_completed=Count('userchallenge', filter=Q(userchallenge__status='Completed')),
                points=Sum(
                    Case(
                        When(userchallenge__status='Completed', userchallenge__challenge__difficulty='Easy', then=50),
                        When(userchallenge__status='Completed', userchallenge__challenge__difficulty='Medium', then=100),
                        When(userchallenge__status='Completed', userchallenge__challenge__difficulty='Hard', then=200),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ).order_by('-challenges_completed')
            
            # Prepare the response data
            leaderboard_data = []
            for user in users_with_challenges:
                leaderboard_data.append({
                    'id': user.id,
                    'username': user.username,
                    'profile_image': user.profile_image,
                    'challenges_completed': user.challenges_completed,
                    'points': user.points or 0  # Use 0 if points is None
                })
            
            return Response(leaderboard_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve leaderboard data: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class LeaderboardPointsView(APIView):
    """
    API endpoint for retrieving the leaderboard based on points
    """
    def get(self, request):
        try:
            # Get all users with their points and completed challenges
            users_with_points = User.objects.annotate(
                points=Sum(
                    Case(
                        When(userchallenge__status='Completed', userchallenge__challenge__difficulty='Easy', then=50),
                        When(userchallenge__status='Completed', userchallenge__challenge__difficulty='Medium', then=100),
                        When(userchallenge__status='Completed', userchallenge__challenge__difficulty='Hard', then=200),
                        default=0,
                        output_field=IntegerField()
                    )
                ),
                challenges_completed=Count('userchallenge', filter=Q(userchallenge__status='Completed'))
            ).order_by('-points')
            
            # Prepare the response data
            leaderboard_data = []
            for user in users_with_points:
                leaderboard_data.append({
                    'id': user.id,
                    'username': user.username,
                    'profile_image': user.profile_image,
                    'challenges_completed': user.challenges_completed,
                    'points': user.points or 0  # Use 0 if points is None
                })
            
            return Response(leaderboard_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve leaderboard data: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# This function is no longer needed as we calculate points directly in the query
