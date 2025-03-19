from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Challenge, Challenge_Category, Submission, Notification
from .serializers import SubmissionSerializer, ChallengeSerializer, UserSerializer
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db.models import Count
import json

class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, user):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))

@method_decorator(csrf_protect, name='dispatch')
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
            
            stats = {
                'totalUsers': total_users,
                'totalChallenges': total_challenges,
                'pendingSubmissions': pending_submissions,
                'approvedSubmissions': approved_submissions,
                'rejectedSubmissions': rejected_submissions
            }
            
            return Response(stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve admin stats: {str(e)}'},
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
                    'status': submission.status
                })
            
            return Response(submissions_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve recent submissions: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminSubmissionsView(APIView):
    """
    API endpoint for retrieving and filtering submissions for admin
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
            
            # Prepare the response data
            submissions_data = []
            for submission in submissions:
                submissions_data.append({
                    'id': submission.id,
                    'username': submission.user.username,
                    'user_id': submission.user.id,
                    'challenge_name': submission.challenge.name,
                    'challenge_id': submission.challenge.id,
                    'file_url': submission.file_url,
                    'submitted_at': submission.submitted_at,
                    'time_taken': str(submission.time_taken),
                    'status': submission.status,
                    'reject_reason': getattr(submission, 'reject_reason', None)
                })
            
            return Response(submissions_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve submissions: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminApproveSubmissionView(APIView):
    """
    API endpoint for approving a submission
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request, submission_id):
        try:
            # Get the submission
            submission = Submission.objects.get(id=submission_id)
            
            # Update the submission status
            submission.status = 'approved'
            submission.save()
            
            # Create a notification for the user
            Notification.objects.create(
                user=submission.user,
                title='Run Submission Approved',
                content=f'Your submission for "{submission.challenge.name}" has been approved and added to the leaderboard!',
                type='success',
                challenge=submission.challenge,
                status='approved'
            )
            
            return Response({'message': 'Submission approved successfully'}, status=status.HTTP_200_OK)
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
    API endpoint for rejecting a submission
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
            
            # Update the submission status and reason
            submission.status = 'rejected'
            submission.reject_reason = reason
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
            
            return Response({'message': 'Submission rejected successfully'}, status=status.HTTP_200_OK)
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

@method_decorator(csrf_protect, name='dispatch')
class AdminChallengesView(APIView):
    """
    API endpoint for managing challenges
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
            
            # Prepare the response data
            challenges_data = []
            for challenge in challenges:
                challenges_data.append({
                    'id': challenge.id,
                    'name': challenge.name,
                    'details': challenge.details,
                    'difficulty': challenge.difficulty,
                    'category': challenge.category.name
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
            
            # Create challenge
            challenge = Challenge.objects.create(
                name=name,
                details=details,
                difficulty=difficulty,
                category=category
            )
            
            # Return the created challenge
            return Response({
                'id': challenge.id,
                'name': challenge.name,
                'details': challenge.details,
                'difficulty': challenge.difficulty,
                'category': challenge.category.name
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'Failed to create challenge: {str(e)}'},
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
            
            # Return the challenge data
            return Response({
                'id': challenge.id,
                'name': challenge.name,
                'details': challenge.details,
                'difficulty': challenge.difficulty,
                'category': challenge.category.name
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
            challenge.name = name
            challenge.details = details
            challenge.difficulty = difficulty
            challenge.category = category
            challenge.save()
            
            # Return the updated challenge
            return Response({
                'id': challenge.id,
                'name': challenge.name,
                'details': challenge.details,
                'difficulty': challenge.difficulty,
                'category': challenge.category.name
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
    
    def delete(self, request, challenge_id):
        try:
            # Get the challenge
            challenge = Challenge.objects.get(id=challenge_id)
            
            # Delete the challenge
            challenge.delete()
            
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
                categories_data.append({
                    'id': category.id,
                    'name': category.name
                })
            
            return Response(categories_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve categories: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminUsersView(APIView):
    """
    API endpoint for managing users
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Get all users
            users = User.objects.all().order_by('username')
            
            # Prepare the response data
            users_data = []
            for user in users:
                # Count completed challenges
                completed_challenges = Submission.objects.filter(user=user, status='approved').count()
                
                users_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'profile_image': user.profile_image,
                    'date_joined': user.date_joined,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'completed_challenges': completed_challenges
                })
            
            return Response(users_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve users: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_protect, name='dispatch')
class AdminUserDetailView(APIView):
    """
    API endpoint for managing a specific user
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, user_id):
        try:
            # Get the user
            user = User.objects.get(id=user_id)
            
            # Count completed challenges
            completed_challenges = Submission.objects.filter(user=user, status='approved').count()
            
            # Return the user data
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_image': user.profile_image,
                'date_joined': user.date_joined,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'completed_challenges': completed_challenges
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
            
            # Return the updated user
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_image': user.profile_image,
                'date_joined': user.date_joined,
                'is_active': user.is_active,
                'is_staff': user.is_staff
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

@method_decorator(csrf_protect, name='dispatch')
class AdminSettingsView(APIView):
    """
    API endpoint for managing site settings
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        try:
            # Return default settings for now
            # In a real implementation, these would be stored in a database
            settings = {
                'site_name': 'Elden Ring Challenges',
                'site_description': 'A platform for Elden Ring challenge runs',
                'enable_registrations': True,
                'enable_submissions': True,
                'maintenance_mode': False,
                'notification_email': 'admin@eldenring.com',
                'max_submissions_per_day': 5,
                'auto_approve_submissions': False
            }
            
            return Response(settings, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to retrieve settings: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request):
        try:
            # In a real implementation, these would be saved to a database
            # For now, just validate the data and return success
            
            # Validate required fields
            required_fields = [
                'site_name', 'site_description', 'notification_email', 
                'max_submissions_per_day'
            ]
            
            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {'error': f'{field} is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validate boolean fields
            boolean_fields = [
                'enable_registrations', 'enable_submissions', 
                'maintenance_mode', 'auto_approve_submissions'
            ]
            
            for field in boolean_fields:
                if field in request.data and not isinstance(request.data[field], bool):
                    return Response(
                        {'error': f'{field} must be a boolean'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validate numeric fields
            if 'max_submissions_per_day' in request.data:
                try:
                    max_submissions = int(request.data['max_submissions_per_day'])
                    if max_submissions < 1:
                        return Response(
                            {'error': 'max_submissions_per_day must be at least 1'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except (ValueError, TypeError):
                    return Response(
                        {'error': 'max_submissions_per_day must be a number'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Return success
            return Response({'message': 'Settings updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Failed to update settings: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
