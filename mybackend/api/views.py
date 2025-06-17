from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Challenge, User, Submission,  DiscussionThread, Comment
from .serializers import ChallengeSerializer, SubmissionSerializer, DiscussionThreadSerializer, CommentSerializer, UserSerializer
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout as django_logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.http import JsonResponse
from django.middleware.csrf import get_token
import random
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .models import Challenge, User, Submission, DiscussionThread, Comment, Notification
from .validators import (
    validate_username, validate_email_format, validate_submission_url,
    validate_time_format, sanitize_text_input, validate_challenge_data,
    validate_rejection_reason
)
import logging

logger = logging.getLogger('api')

# Try to import SiteSettings, create a mock if it doesn't exist
try:
    from .models import SiteSettings
except ImportError:
    # Create a mock SiteSettings class if the model doesn't exist
    class SiteSettings:
        @classmethod
        def get_settings(cls):
            # Return default settings
            class MockSettings:
                enable_registrations = True
                enable_submissions = True
                maintenance_mode = False
                max_submissions_per_day = 5
                auto_approve_submissions = False
            return MockSettings()

User = get_user_model()

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GETCSRFToken(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, format=None):
        return Response({'csrftoken': get_token(request)})

class SimpleAPIView(APIView):
    def get(self, request):
        return Response({"message": "Hello from Django!"})
    
@method_decorator(csrf_protect, name='dispatch')
class SignupAPIView(APIView):
    def post(self, request):
        # Check if registrations are enabled
        try:
            settings = SiteSettings.get_settings()
            if not settings.enable_registrations:
                return Response(
                    {"error": "User registrations are currently disabled"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        except Exception as e:
            print(f"Error checking settings: {e}")
            # Continue with default behavior if settings check fails
        
        # Get and validate input
        email = request.data.get('email', '').strip().lower()
        username = request.data.get('username', '').strip().lower()
        password = request.data.get('password', '')

        # Basic validation
        if not username or not email or not password:
            return Response(
                {"error": "Username, email, and password are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Username validation
        if len(username) < 3 or len(username) > 30:
            return Response(
                {"error": "Username must be between 3 and 30 characters"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Email validation (basic)
        if '@' not in email or '.' not in email:
            return Response(
                {"error": "Please enter a valid email address"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Password validation
        if len(password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters long"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the email or username already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email is already in use"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username is already in use"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create a new user
            user = User.objects.create_user(
                email=email, 
                username=username, 
                password=password
            )
            
            print(f"User created successfully: {user.username} ({user.email})")
            
            return Response({
                "message": "Signup successful!",
                "user": {
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return Response(
                {"error": "Failed to create account. Please try again."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
@method_decorator(csrf_protect, name='dispatch')
class LoginAPIView(APIView):
    def post(self, request):
        print("Login View - POST request")
        print("Request Data:", request.data)

        username = request.data.get('username', '').strip().lower()
        password = request.data.get('password', '')
        
        # Validate input
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not user.is_active:
                return Response({"error": "Account is disabled"}, status=status.HTTP_401_UNAUTHORIZED)
            
            login(request, user)
            response = Response({
                "message": "Login successful!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser
                },
                "redirect": "/home"
            }, status=status.HTTP_200_OK)
            return response
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_protect, name='dispatch')
class LogoutAPIView(APIView):
    def post(self, request):
        # Logout the user
        django_logout(request)

        # Create a response object
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        
        # Clear session ID cookie
        response.delete_cookie('sessionid', path='/')
        
        # Optionally clear CSRF token cookie
        response.delete_cookie('csrftoken', path='/')

        return response

# Generate token for password reset
token_generator = PasswordResetTokenGenerator()

@method_decorator(csrf_protect, name='dispatch')
class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        
        # Use the configured frontend URL
        reset_link = f"{settings.FRONTEND_URL}/password-reset-confirm/{uid}/{token}/"

        send_mail(
            'Password Reset Request',
            f'Use the link below to reset your password:\n{reset_link}',
            'no-reply@example.com',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Password reset link sent"}, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if token_generator.check_token(user, token):
                new_password = request.data.get('password')
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView):
    """
    Modified to work without the user profile feature
    """
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            # Return minimal user data needed for the app to function
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

class HomeAPIView(APIView):
    def post(self, request):
        return Response({"message": "Home Page!"})

@method_decorator(csrf_protect, name='dispatch')
class ChallengeAPIView(APIView):
    def get(self, request, challenge_id=None):
        if challenge_id:
            try:
                challenge = Challenge.objects.get(id=challenge_id)
                serializer = ChallengeSerializer(challenge)
                
                # Check if the user has completed this challenge
                completed = False
                if request.user.is_authenticated:
                    completed = Submission.objects.filter(
                        user=request.user,
                        challenge=challenge,
                        status='approved'
                    ).exists()
                
                data = serializer.data
                data['completed'] = completed
                return Response(data)
            except Challenge.DoesNotExist:
                return Response(
                    {"error": "Challenge not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            challenges = Challenge.objects.all()
            serializer = ChallengeSerializer(challenges, many=True)
            
            # If user is authenticated, check completion status for each challenge
            if request.user.is_authenticated:
                user_completed_challenges = set(
                    Submission.objects.filter(
                        user=request.user,
                        status='approved'
                    ).values_list('challenge_id', flat=True)
                )
                
                # Add completion status to each challenge
                data = serializer.data
                for challenge_data in data:
                    challenge_data['completed'] = challenge_data['id'] in user_completed_challenges
                
                return Response(data)
            else:
                # For non-authenticated users, all challenges are not completed
                data = serializer.data
                for challenge_data in data:
                    challenge_data['completed'] = False
                
                return Response(data)
        
@method_decorator(csrf_protect, name='dispatch')
class ChallengeDetailView(generics.RetrieveAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

# FIXED: Updated ChallengeSubmissionsView to return proper JSON
class ChallengeSubmissionsView(APIView):
    """
    Fixed API view for retrieving challenge submissions
    """
    def get(self, request):
        try:
            challenge_id = request.GET.get('challenge')
            if not challenge_id:
                return Response(
                    {"error": "Challenge ID is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify challenge exists
            try:
                challenge = Challenge.objects.get(id=challenge_id)
            except Challenge.DoesNotExist:
                return Response(
                    {"error": "Challenge not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get approved submissions for this challenge, ordered by time
            submissions = Submission.objects.filter(
                challenge_id=challenge_id, 
                status='approved'
            ).order_by('time_taken')[:10]
            
            serializer = SubmissionSerializer(submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in ChallengeSubmissionsView: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
@method_decorator(csrf_protect, name='dispatch')
class SubmitRunAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        print("Submit Run View")
        print(f"Request Headers: {request.headers}")
        print(f"Request Data: {request.data}")

        challenge_id = request.data.get('challenge')
        file_url = request.data.get('file_url')
        user_id = request.data.get('user')

        if not challenge_id or not file_url or not user_id:
            return Response({"error": "Challenge ID, file URL, and user ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the challenge and user objects
            challenge = Challenge.objects.get(id=challenge_id)
            user = User.objects.get(id=user_id)
            
            # Check if user has reached daily submission limit
            settings = SiteSettings.get_settings()
            today = timezone.now().date()
            daily_submissions = Submission.objects.filter(
                user=user, 
                submitted_at__date=today
            ).count()
            
            if daily_submissions >= settings.max_submissions_per_day:
                return Response({
                    "error": f"Daily submission limit reached ({settings.max_submissions_per_day} per day)"
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

            # Create the submission
            submission = Submission.objects.create(
                challenge=challenge,
                file_url=file_url,
                user=user,
                time_taken=request.data.get('time_taken', timedelta())
            )
            
            # Check if auto-approval is enabled
            if settings.auto_approve_submissions:
                # Auto-approve the submission
                points_to_award = challenge.get_total_points()
                submission.status = 'approved'
                submission.points_awarded = points_to_award
                submission.approved_at = timezone.now()
                submission.save()
                
                # Update user's total points and challenge count
                user.update_points_and_challenges()
                
                # Create a success notification
                Notification.objects.create(
                    user=user,
                    title='Run Submission Auto-Approved',
                    content=f'Your submission for "{challenge.name}" has been automatically approved and added to the leaderboard! You earned {points_to_award} points.',
                    type='success',
                    challenge=challenge,
                    status='approved'
                )
                
                return Response({
                    "message": "Submission automatically approved!",
                    "points_awarded": points_to_award,
                    "status": "approved"
                }, status=status.HTTP_201_CREATED)
            else:
                # Manual approval required
                # Create a pending notification
                Notification.objects.create(
                    user=user,
                    title='Run Submission Received',
                    content=f'Your submission for "{challenge.name}" has been received and is pending admin review.',
                    type='info',
                    challenge=challenge,
                    status='pending'
                )
                
                return Response({
                    "message": "Submission received and pending approval!",
                    "status": "pending"
                }, status=status.HTTP_201_CREATED)
                
        except Challenge.DoesNotExist:
            return Response({"error": "Challenge not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error creating submission: {e}")
            return Response({"error": "Failed to create submission"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ThreadListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id', None)
        if category_id:
            threads = DiscussionThread.objects.filter(category_id=category_id)
        else:
            threads = DiscussionThread.objects.all()
        
        serializer = DiscussionThreadSerializer(threads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ThreadDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, thread_id, *args, **kwargs):
        try:
            thread = DiscussionThread.objects.get(id=thread_id)
            comments = Comment.objects.filter(thread=thread).order_by('created_at')
            
            thread_serializer = DiscussionThreadSerializer(thread)
            comments_serializer = CommentSerializer(comments, many=True)
            
            # Prepare response data
            data = {
                'thread': thread_serializer.data,
                'comments': comments_serializer.data,
                'categoryName': thread.category.name
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except DiscussionThread.DoesNotExist:
            return Response({'detail': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)
        

# Add this to api/views.py if needed

from django.shortcuts import render
from django.views.generic import TemplateView

class ReactAppView(TemplateView):
    """
    Serves the React app for all non-API routes
    """
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data your React app might need
        return context