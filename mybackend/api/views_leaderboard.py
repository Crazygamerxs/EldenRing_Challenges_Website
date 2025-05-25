# Enhanced views_leaderboard.py with real points system - FIXED

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Case, When, IntegerField, Q, F
from .models import User, Challenge, Submission, UserChallenge
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect, name='dispatch')
class LeaderboardChallengesView(APIView):
    """
    API endpoint for retrieving the leaderboard based on completed challenges
    Uses real data from approved submissions
    """
    def get(self, request):
        try:
            # Get all users with approved submissions, ordered by challenge count then points
            users_with_challenges = User.objects.annotate(
                approved_submissions_count=Count(
                    'submission', 
                    filter=Q(submission__status='approved')
                )
            ).filter(
                approved_submissions_count__gt=0  # Only users with at least one approved submission
            ).order_by(
                '-approved_submissions_count',  # Most challenges completed first
                '-total_points',                # Then by points as tiebreaker
                'username'                      # Then alphabetically
            )
            
            # Prepare the response data
            leaderboard_data = []
            for rank, user in enumerate(users_with_challenges, 1):
                # Get additional stats for this user
                recent_submission = Submission.objects.filter(
                    user=user, 
                    status='approved'
                ).order_by('-approved_at').first()
                
                leaderboard_data.append({
                    'rank': rank,
                    'id': user.id,
                    'username': user.username,
                    'challenges_completed': user.challenges_completed_count,
                    'points': user.total_points,
                    'last_completion': recent_submission.approved_at if recent_submission else None,
                    'most_recent_challenge': recent_submission.challenge.name if recent_submission else None
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
    Uses real data from approved submissions
    """
    def get(self, request):
        try:
            # Get all users with points, ordered by points then challenge count
            users_with_points = User.objects.filter(
                total_points__gt=0  # Only users with points
            ).order_by(
                '-total_points',                    # Highest points first
                '-challenges_completed_count',      # Then by challenge count as tiebreaker
                'username'                          # Then alphabetically
            )
            
            # Prepare the response data
            leaderboard_data = []
            for rank, user in enumerate(users_with_points, 1):
                # Get additional stats for this user
                recent_submission = Submission.objects.filter(
                    user=user, 
                    status='approved'
                ).order_by('-approved_at').first()
                
                # Get highest point challenge completed
                highest_point_submission = Submission.objects.filter(
                    user=user,
                    status='approved'
                ).order_by('-points_awarded').first()
                
                leaderboard_data.append({
                    'rank': rank,
                    'id': user.id,
                    'username': user.username,
                    'challenges_completed': user.challenges_completed_count,
                    'points': user.total_points,
                    'last_completion': recent_submission.approved_at if recent_submission else None,
                    'highest_point_challenge': highest_point_submission.challenge.name if highest_point_submission else None,
                    'highest_points_earned': highest_point_submission.points_awarded if highest_point_submission else 0
                })
            
            return Response(leaderboard_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve leaderboard data: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class LeaderboardStatsView(APIView):
    """
    API endpoint for retrieving leaderboard statistics
    """
    def get(self, request):
        try:
            # Get overall statistics
            total_users = User.objects.filter(total_points__gt=0).count()
            total_points_awarded = User.objects.aggregate(
                total=Sum('total_points')
            )['total'] or 0
            
            total_challenges_completed = Submission.objects.filter(
                status='approved'
            ).count()
            
            # Get top performers
            top_user_by_points = User.objects.filter(
                total_points__gt=0
            ).order_by('-total_points').first()
            
            top_user_by_challenges = User.objects.filter(
                challenges_completed_count__gt=0
            ).order_by('-challenges_completed_count').first()
            
            # Get most popular challenges
            popular_challenges = Challenge.objects.annotate(
                completion_count=Count('submission', filter=Q(submission__status='approved'))
            ).filter(completion_count__gt=0).order_by('-completion_count')[:5]
            
            # Get highest point challenges
            highest_point_challenges = Challenge.objects.filter(
                submission__status='approved'
            ).distinct().order_by('-base_points')[:5]
            
            stats = {
                'total_users_with_points': total_users,
                'total_points_awarded': total_points_awarded,
                'total_challenges_completed': total_challenges_completed,
                'top_user_by_points': {
                    'username': top_user_by_points.username,
                    'points': top_user_by_points.total_points
                } if top_user_by_points else None,
                'top_user_by_challenges': {
                    'username': top_user_by_challenges.username,
                    'challenges': top_user_by_challenges.challenges_completed_count
                } if top_user_by_challenges else None,
                'popular_challenges': [
                    {
                        'name': challenge.name,
                        'completions': challenge.completion_count,
                        'points': challenge.get_total_points()
                    } for challenge in popular_challenges
                ],
                'highest_point_challenges': [
                    {
                        'name': challenge.name,
                        'points': challenge.get_total_points(),
                        'difficulty': challenge.difficulty,
                        'is_combination': challenge.is_combination
                    } for challenge in highest_point_challenges
                ]
            }
            
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve leaderboard stats: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class UserLeaderboardStatsView(APIView):
    """
    API endpoint for retrieving a specific user's leaderboard position and stats
    """
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            
            # Get user's rank by points
            points_rank = User.objects.filter(
                total_points__gt=user.total_points
            ).count() + 1
            
            # Get user's rank by challenges completed
            challenges_rank = User.objects.filter(
                challenges_completed_count__gt=user.challenges_completed_count
            ).count() + 1
            
            # Get user's recent submissions
            recent_submissions = Submission.objects.filter(
                user=user,
                status='approved'
            ).order_by('-approved_at')[:5]
            
            # Get user's challenge type breakdown
            challenge_breakdown = {}
            for submission in Submission.objects.filter(user=user, status='approved'):
                category = submission.challenge.category.name
                if category not in challenge_breakdown:
                    challenge_breakdown[category] = {
                        'count': 0,
                        'points': 0
                    }
                challenge_breakdown[category]['count'] += 1
                challenge_breakdown[category]['points'] += submission.points_awarded
            
            stats = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'total_points': user.total_points,
                    'challenges_completed': user.challenges_completed_count
                },
                'rankings': {
                    'points_rank': points_rank,
                    'challenges_rank': challenges_rank
                },
                'recent_submissions': [
                    {
                        'challenge_name': sub.challenge.name,
                        'points_awarded': sub.points_awarded,
                        'approved_at': sub.approved_at,
                        'difficulty': sub.challenge.difficulty
                    } for sub in recent_submissions
                ],
                'challenge_breakdown': challenge_breakdown
            }
            
            return Response(stats, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve user stats: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )