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

User = get_user_model()

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GETCSRFToken(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, format=None):
        return Response({'csrftoken': get_token(request)})

class SimpleAPIView(APIView):
    def get(self, request):
        return Response({"message": "Hello from Django!"})
    
class SignupAPIView(APIView):
    def post(self, request):
        email = request.data.get('email').strip().lower()
        username = request.data.get('username').strip().lower()
        password = request.data.get('password')

        # Check if the email or username already exists
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email is already in use"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username is already in use"}, status=status.HTTP_400_BAD_REQUEST)

        # Define your profile pictures URLs
        profile_pics = [
            static('main/images/profile_pic/pp_1.png'),
            static('main/images/profile_pic/pp_2.png'),
            static('main/images/profile_pic/pp_3.png'),
        ]

        # Randomly select a profile picture
        profile_pic_url = random.choice(profile_pics)

        # Create a new user with the selected profile picture
        user = User.objects.create_user(email=email, username=username, password=password, profile_image=profile_pic_url)
        
        return Response({"message": "Signup successful!"}, status=status.HTTP_201_CREATED)

@method_decorator(csrf_protect, name='dispatch')
class LoginAPIView(APIView):
    def post(self, request):
        print("Login View - POST request")
        print("Request Data:", request.data)  # Log request data

        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            response = Response({
                "message": "Login successful!",
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
        response.delete_cookie('sessionid', path='/')  # Default path
        
        # Optionally clear CSRF token cookie
        response.delete_cookie('csrftoken', path='/')  # Path should match if set

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



class HomeAPIView(APIView):
    def post(self, request):
        return Response({"message": "Home Page!"})

@method_decorator(csrf_protect, name='dispatch')
class ChallengeAPIView(APIView):
    def get(self, request, challenge_id=None):
        if challenge_id:
            challenge = Challenge.objects.get(id=challenge_id)
            serializer = ChallengeSerializer(challenge)
            return Response(serializer.data)
        else:
            challenges = Challenge.objects.all()
            serializer = ChallengeSerializer(challenges, many=True)
            return Response(serializer.data)
        

class ChallengeDetailView(generics.RetrieveAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

class ChallengeSubmissionsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        challenge_id = self.request.query_params.get('challenge')
        return Submission.objects.filter(challenge_id=challenge_id)

class SubmitRunAPIView(APIView):
    def post(self, request):
        print("Submit Run View")
        print(f"Request Headers: {request.headers}")
        print(f"Request Data: {request.data}")

        challenge_id = request.data.get('challenge')
        file_url = request.data.get('file_url')
        user_id = request.data.get('user')  # Get the user ID from the request

        if not challenge_id or not file_url or not user_id:
            return Response({"error": "Challenge ID, file URL, and user ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the submission
            submission = Submission.objects.create(
                challenge_id=challenge_id,
                file_url=file_url,
                user_id=user_id,  # Include the user ID
                # time_taken will use the default value (timedelta())
            )
            return Response({"message": "Submission successful!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error creating submission: {e}")
            return Response({"error": "Failed to create submission"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ThreadListView(APIView):
    permission_classes = [IsAuthenticated]

    print("ThreadListView")
    def get(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id', None)
        if category_id:
            threads = DiscussionThread.objects.filter(category_id=category_id)
        else:
            threads = DiscussionThread.objects.all()
        
        serializer = DiscussionThreadSerializer(threads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  # Co
    
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
                'categoryName': thread.category.name  # Include categoryName
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except DiscussionThread.DoesNotExist:
            return Response({'detail': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)
