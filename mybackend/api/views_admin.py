from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Challenge, Challenge_Category, Submission, Notification, SiteSettings  # ADDED SiteSettings
from .serializers import SubmissionSerializer, ChallengeSerializer, UserSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
import json
from .models import User, Challenge, Challenge_Category, Submission, Notification, SiteSettings


class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, user):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))

class AdminStatsView(APIView):
    """
    API endpoint for retrieving admin dashboard statistics
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Count total users
            total_users = User.objects.count()
            
            # Count total challenges
            total_challenges = Challenge.objects.count()
            
            # Count submissions by status
            pending_submissions = Submission.objects.filter(status='pending').count()
            approved_submissions = Submission.objects.filter(status='approved').count()
            rejected_submissions = Submission.objects.filter(status='rejected').count()
            
            # Points statistics
            total_points_awarded = sum(sub.points_awarded for sub in Submission.objects.filter(status='approved'))
            average_points_per_challenge = Challenge.objects.aggregate(avg_points=Avg('base_points'))['avg_points'] or 0
            
            stats = {
                'totalUsers': total_users,
                'totalChallenges': total_challenges,
                'pendingSubmissions': pending_submissions,
                'approvedSubmissions': approved_submissions,
                'rejectedSubmissions': rejected_submissions,
                'totalPointsAwarded': total_points_awarded,
                'averagePointsPerChallenge': round(average_points_per_challenge, 1)
            }
            
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve admin stats: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminSettingsView(APIView):
    """
    API endpoint for managing site settings - NOW WITH REAL PERSISTENCE
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Get the actual settings from database
            settings = SiteSettings.get_settings()
            
            settings_data = {
                'site_name': settings.site_name,
                'site_description': settings.site_description,
                'enable_registrations': settings.enable_registrations,
                'enable_submissions': settings.enable_submissions,
                'maintenance_mode': settings.maintenance_mode,
                'notification_email': settings.notification_email,
                'max_submissions_per_day': settings.max_submissions_per_day,
                'auto_approve_submissions': settings.auto_approve_submissions
            }
            
            return Response(settings_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve settings: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request):
        try:
            # Get the current settings instance
            settings = SiteSettings.get_settings()
            
            # Validate required fields
            required_fields = [
                'site_name', 'site_description', 'notification_email', 
                'max_submissions_per_day'
            ]
            
            for field in required_fields:
                if field not in request.data or not request.data[field]:
                    return Response(
                        {'error': f'{field} is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validate email format
            try:
                from django.core.validators import validate_email
                validate_email(request.data['notification_email'])
            except:
                return Response(
                    {'error': 'Invalid email format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate numeric fields
            try:
                max_submissions = int(request.data['max_submissions_per_day'])
                if max_submissions < 1 or max_submissions > 100:
                    return Response(
                        {'error': 'max_submissions_per_day must be between 1 and 100'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except (ValueError, TypeError):
                return Response(
                    {'error': 'max_submissions_per_day must be a number'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update settings
            settings.site_name = request.data['site_name']
            settings.site_description = request.data['site_description']
            settings.enable_registrations = request.data.get('enable_registrations', True)
            settings.enable_submissions = request.data.get('enable_submissions', True)  
            settings.maintenance_mode = request.data.get('maintenance_mode', False)
            settings.notification_email = request.data['notification_email']
            settings.max_submissions_per_day = max_submissions
            settings.auto_approve_submissions = request.data.get('auto_approve_submissions', False)
            
            # Save to database
            settings.save()
            
            return Response({'message': 'Settings updated successfully'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to update settings: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminApproveSubmissionView(APIView):
    """
    Enhanced API endpoint for approving a submission with points calculation
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request, submission_id):
        try:
            # Get the submission
            submission = Submission.objects.get(id=submission_id)
            
            # Get admin verified time if provided
            admin_time_str = request.data.get('admin_verified_time')
            
            if admin_time_str:
                try:
                    # Parse the admin time string (HH:MM:SS)
                    time_parts = admin_time_str.split(':')
                    if len(time_parts) == 3:
                        hours = int(time_parts[0])
                        minutes = int(time_parts[1])
                        seconds = int(time_parts[2])
                        
                        if minutes < 60 and seconds < 60 and hours >= 0 and minutes >= 0 and seconds >= 0:
                            submission.admin_verified_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                        else:
                            return Response(
                                {'error': 'Invalid time values in admin verified time'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        return Response(
                            {'error': 'Invalid admin time format. Use HH:MM:SS'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except (ValueError, IndexError):
                    return Response(
                        {'error': 'Invalid admin time format. Use HH:MM:SS'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Calculate and award points
            points_to_award = submission.challenge.get_total_points()
            submission.points_awarded = points_to_award
            
            # Update the submission status
            submission.status = 'approved'
            submission.approved_at = timezone.now()
            submission.approved_by = request.user
            submission.save()
            
            # Update user's total points and challenge count
            submission.user.update_points_and_challenges()
            
            # Create a notification for the user
            Notification.objects.create(
                user=submission.user,
                title='Run Submission Approved',
                content=f'Your submission for "{submission.challenge.name}" has been approved and added to the leaderboard! You earned {points_to_award} points.',
                type='success',
                challenge=submission.challenge,
                status='approved'
            )
            
            return Response({
                'message': 'Submission approved successfully',
                'pointsAwarded': points_to_award,
                'adminVerifiedTime': submission.format_admin_time()
            }, status=status.HTTP_200_OK)
            
        except Submission.DoesNotExist:
            return Response(
                {'error': 'Submission not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to approve submission: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
@method_decorator(csrf_protect, name='dispatch')
class AdminRejectSubmissionView(APIView):
    """
    Enhanced API endpoint for rejecting a submission with points removal
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request, submission_id):
        try:
            # Get the rejection reason from request body
            reason = request.data.get('reason', '')
            
            if not reason:
                return Response(
                    {'error': 'Rejection reason is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the submission
            submission = Submission.objects.get(id=submission_id)
            
            # Remove points if submission was previously approved
            points_removed = 0
            if submission.status == 'approved':
                points_removed = submission.points_awarded
                submission.remove_points()
            
            # Update the submission status and reason
            submission.status = 'rejected'
            submission.reject_reason = reason
            submission.approved_at = None
            submission.approved_by = None
            submission.save()
            
            # Create a notification for the user
            Notification.objects.create(
                user=submission.user,
                title='Run Submission Rejected',
                content=f'Your submission for "{submission.challenge.name}" has been rejected. Reason: {reason}',
                type='error',
                challenge=submission.challenge,
                status='rejected'
            )
            
            response_data = {'message': 'Submission rejected successfully'}
            if points_removed > 0:
                response_data['pointsRemoved'] = points_removed
                response_data['userTotalPoints'] = submission.user.total_points
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Submission.DoesNotExist:
            return Response(
                {'error': 'Submission not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to reject submission: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AdminSubmissionsView(APIView):
    """
    Enhanced API endpoint for retrieving submissions with points information
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Get status filter from query params (default to 'all')
            status_filter = request.query_params.get('status', 'all')
            
            # Filter submissions based on status
            if status_filter != 'all':
                submissions = Submission.objects.filter(status=status_filter).order_by('-submitted_at')
            else:
                submissions = Submission.objects.all().order_by('-submitted_at')
            
            # Prepare the response data with points information
            submissions_data = []
            for submission in submissions:
                submissions_data.append({
                    'id': submission.id,
                    'username': submission.user.username,
                    'user_id': submission.user.id,
                    'challenge_name': submission.challenge.name,
                    'challenge_id': submission.challenge.id,
                    'challenge_difficulty': submission.challenge.difficulty,
                    'challenge_is_combination': submission.challenge.is_combination,
                    'challenge_points': submission.challenge.get_total_points(),
                    'file_url': submission.file_url,
                    'submitted_at': submission.submitted_at,
                    'time_taken': str(submission.time_taken),
                    'user_time': submission.format_time(),  # ADD THIS LINE
                    'admin_verified_time': getattr(submission, 'admin_verified_time', None),  # ADD THIS LINE
                    'status': submission.status,
                    'points_awarded': submission.points_awarded,
                    'approved_at': submission.approved_at,
                    'approved_by': submission.approved_by.username if submission.approved_by else None,
                    'reject_reason': getattr(submission, 'reject_reason', None)
                })
            
            return Response(submissions_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve submissions: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminChallengesView(APIView):
    """
    Enhanced API endpoint for managing challenges with points information
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Get category filter from query params (default to all)
            category_filter = request.query_params.get('category', '')
            
            # Filter challenges based on category
            if category_filter:
                challenges = Challenge.objects.filter(category__name=category_filter).order_by('name')
            else:
                challenges = Challenge.objects.all().order_by('name')
            
            # Prepare the response data with points information
            challenges_data = []
            for challenge in challenges:
                completion_count = Submission.objects.filter(challenge=challenge, status='approved').count()
                
                challenges_data.append({
                    'id': challenge.id,
                    'name': challenge.name,
                    'details': challenge.details,
                    'difficulty': challenge.difficulty,
                    'category': challenge.category.name,
                    'is_dlc': challenge.is_dlc,
                    'is_combination': challenge.is_combination,
                    'base_points': challenge.base_points,
                    'total_points': challenge.get_total_points(),
                    'completion_count': completion_count
                })
            
            return Response(challenges_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve challenges: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        try:
            # Get challenge data from request body
            name = request.data.get('name')
            details = request.data.get('details')
            difficulty = request.data.get('difficulty')
            category_id = request.data.get('category')
            is_dlc = request.data.get('is_dlc', False)
            is_combination = request.data.get('is_combination', False)
            
            # Validate required fields
            if not name or not details or not difficulty or not category_id:
                return Response(
                    {'error': 'All fields are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get category
            try:
                category = Challenge_Category.objects.get(id=category_id)
            except Challenge_Category.DoesNotExist:
                return Response(
                    {'error': 'Category not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Create challenge (points will be auto-calculated in save method)
            challenge = Challenge.objects.create(
                name=name,
                details=details,
                difficulty=difficulty,
                category=category,
                is_dlc=is_dlc,
                is_combination=is_combination
            )
            
            # Return the created challenge with points information
            return Response({
                'id': challenge.id,
                'name': challenge.name,
                'details': challenge.details,
                'difficulty': challenge.difficulty,
                'category': challenge.category.name,
                'is_dlc': challenge.is_dlc,
                'is_combination': challenge.is_combination,
                'base_points': challenge.base_points,
                'total_points': challenge.get_total_points()
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'Failed to create challenge: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminUsersView(APIView):
    """
    Enhanced API endpoint for managing users with points information
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Get all users
            users = User.objects.all().order_by('-total_points', 'username')
            
            # Prepare the response data with points information
            users_data = []
            for user in users:
                users_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'date_joined': user.date_joined,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'total_points': user.total_points,
                    'challenges_completed_count': user.challenges_completed_count,
                    'pending_submissions': Submission.objects.filter(user=user, status='pending').count(),
                    'approved_submissions': Submission.objects.filter(user=user, status='approved').count(),
                    'rejected_submissions': Submission.objects.filter(user=user, status='rejected').count()
                })
            
            return Response(users_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve users: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminRecentSubmissionsView(APIView):
    """
    API endpoint for retrieving recent submissions for admin dashboard
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Get recent submissions (limit to 5)
            recent_submissions = Submission.objects.all().order_by('-submitted_at')[:5]
            
            # Prepare the response data
            submissions_data = []
            for submission in recent_submissions:
                submissions_data.append({
                    'id': submission.id,
                    'username': submission.user.username,
                    'challenge_name': submission.challenge.name,
                    'challenge_id': submission.challenge.id,
                    'submitted_at': submission.submitted_at,
                    'status': submission.status,
                    'points_potential': submission.challenge.get_total_points(),
                    'points_awarded': submission.points_awarded
                })
            
            return Response(submissions_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve recent submissions: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminChallengeDetailView(APIView):
    """
    API endpoint for managing a specific challenge
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, challenge_id):
        try:
            # Get the challenge
            challenge = Challenge.objects.get(id=challenge_id)
            
            # Return the challenge data with points information
            return Response({
                'id': challenge.id,
                'name': challenge.name,
                'details': challenge.details,
                'difficulty': challenge.difficulty,
                'category': challenge.category.name,
                'is_dlc': challenge.is_dlc,
                'is_combination': challenge.is_combination,
                'base_points': challenge.base_points,
                'total_points': challenge.get_total_points()
            }, status=status.HTTP_200_OK)
        except Challenge.DoesNotExist:
            return Response(
                {'error': 'Challenge not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve challenge: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, challenge_id):
        try:
            # Get the challenge
            challenge = Challenge.objects.get(id=challenge_id)
            
            # Update challenge data
            name = request.data.get('name')
            details = request.data.get('details')
            difficulty = request.data.get('difficulty')
            category_id = request.data.get('category')
            is_dlc = request.data.get('is_dlc', False)
            is_combination = request.data.get('is_combination', False)
            
            # Validate required fields
            if not name or not details or not difficulty or not category_id:
                return Response(
                    {'error': 'All fields are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get category
            try:
                category = Challenge_Category.objects.get(id=category_id)
            except Challenge_Category.DoesNotExist:
                return Response(
                    {'error': 'Category not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Update challenge
            old_points = challenge.base_points
            challenge.name = name
            challenge.details = details
            challenge.difficulty = difficulty
            challenge.category = category
            challenge.is_dlc = is_dlc
            challenge.is_combination = is_combination
            challenge.base_points = 0  # Reset to trigger recalculation
            challenge.save()  # This will recalculate points
            
            # If points changed, update all related submissions and users
            if old_points != challenge.base_points:
                self._update_related_submissions(challenge)
            
            # Return the updated challenge
            return Response({
                'id': challenge.id,
                'name': challenge.name,
                'details': challenge.details,
                'difficulty': challenge.difficulty,
                'category': challenge.category.name,
                'is_dlc': challenge.is_dlc,
                'is_combination': challenge.is_combination,
                'base_points': challenge.base_points,
                'total_points': challenge.get_total_points()
            }, status=status.HTTP_200_OK)
        except Challenge.DoesNotExist:
            return Response(
                {'error': 'Challenge not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to update challenge: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _update_related_submissions(self, challenge):
        """Update points for all approved submissions of this challenge"""
        approved_submissions = Submission.objects.filter(challenge=challenge, status='approved')
        
        for submission in approved_submissions:
            old_points = submission.points_awarded
            new_points = challenge.get_total_points()
            
            if old_points != new_points:
                submission.points_awarded = new_points
                submission.save()
                
                # Update user's total points
                submission.user.update_points_and_challenges()
    
    def delete(self, request, challenge_id):
        try:
            # Get the challenge
            challenge = Challenge.objects.get(id=challenge_id)
            
            # Get all users who completed this challenge to update their points
            users_to_update = set()
            for submission in Submission.objects.filter(challenge=challenge, status='approved'):
                users_to_update.add(submission.user)
            
            # Delete the challenge (this will cascade to submissions)
            challenge.delete()
            
            # Update affected users' points
            for user in users_to_update:
                user.update_points_and_challenges()
            
            return Response({'message': 'Challenge deleted successfully'}, status=status.HTTP_200_OK)
        except Challenge.DoesNotExist:
            return Response(
                {'error': 'Challenge not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to delete challenge: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminCategoriesView(APIView):
    """
    API endpoint for retrieving challenge categories
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Get all categories
            categories = Challenge_Category.objects.all().order_by('name')
            
            # Prepare the response data
            categories_data = []
            for category in categories:
                challenges_count = Challenge.objects.filter(category=category).count()
                total_points = sum(c.get_total_points() for c in Challenge.objects.filter(category=category))
                
                categories_data.append({
                    'id': category.id,
                    'name': category.name,
                    'challenges_count': challenges_count,
                    'total_points': total_points
                })
            
            return Response(categories_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve categories: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminUserDetailView(APIView):
    """
    API endpoint for managing a specific user with points information
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, user_id):
        try:
            # Get the user
            user = User.objects.get(id=user_id)
            
            # Get submission statistics
            submissions = Submission.objects.filter(user=user)
            pending_count = submissions.filter(status='pending').count()
            approved_count = submissions.filter(status='approved').count()
            rejected_count = submissions.filter(status='rejected').count()
            
            # Return the user data with points information
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'total_points': user.total_points,
                'challenges_completed': user.challenges_completed_count,
                'pending_submissions': pending_count,
                'approved_submissions': approved_count,
                'rejected_submissions': rejected_count
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve user: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, user_id):
        try:
            # Get the user
            user = User.objects.get(id=user_id)
            
            # Update user data
            username = request.data.get('username')
            email = request.data.get('email')
            is_active = request.data.get('is_active')
            is_staff = request.data.get('is_staff')
            
            # Validate required fields
            if not username or not email:
                return Response(
                    {'error': 'Username and email are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update user
            user.username = username
            user.email = email
            
            # Only update is_active and is_staff if they are provided
            if is_active is not None:
                user.is_active = is_active
            
            if is_staff is not None:
                user.is_staff = is_staff
            
            user.save()
            
            # Return the updated user with points information
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'total_points': user.total_points,
                'challenges_completed_count': user.challenges_completed_count
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to update user: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminUserStatusView(APIView):
    """
    API endpoint for updating a user's active status
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request, user_id):
        try:
            # Get the user
            user = User.objects.get(id=user_id)
            
            # Get the new status from request body
            is_active = request.data.get('is_active')
            
            if is_active is None:
                return Response(
                    {'error': 'is_active field is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update user status
            user.is_active = is_active
            user.save()
            
            return Response({'message': f'User status updated to {"active" if is_active else "inactive"}'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to update user status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
