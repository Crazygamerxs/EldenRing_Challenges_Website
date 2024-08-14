from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Challenge, User, Submission,  DiscussionThread
from .serializers import ChallengeSerializer, SubmissionSerializer, DiscussionThreadSerializer
from django.contrib.auth import get_user_model, authenticate, login
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random
from django.templatetags.static import static
from rest_framework.authtoken.models import Token


User = get_user_model()

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


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Generate or get the authentication token
            token, created = Token.objects.get_or_create(user=user)
            
            # Create a response with a success message and redirect URL
            response = Response({
                "message": "Login successful!",
                "redirect": "/home"
            }, status=status.HTTP_200_OK)
            
            # Set the authentication token in an HTTP-Only cookie
            response.set_cookie(
                'auth_token',  # Cookie name
                token.key,  # Token value
                httponly=True,  # Cookie cannot be accessed via JavaScript
                secure=True,  # Cookie only sent over HTTPS
                samesite='Strict'  # Cookie sent only for same-site requests
            )
            
            return response
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAU)

class HomeAPIView(APIView):
    def post(self, request):
        return Response({"message": "Home Page!"})
    
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
    
class ThreadListView(APIView):
    def get(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id', None)
        if category_id:
            threads = DiscussionThread.objects.filter(category_id=category_id)
        else:
            threads = DiscussionThread.objects.all()
        
        serializer = DiscussionThreadSerializer(threads, many=True)
        return Response(serializer.data)