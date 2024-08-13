from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Challenge, User
from .serializers import ChallengeSerializer
from django.contrib.auth import get_user_model, authenticate, login
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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

        # Create a new user
        user = User.objects.create_user(email=email, username=username, password=password)
        return Response({"message": "Signup successful!"}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Print all cookies received in the request
        print("Received cookies:", request.COOKIES)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("User logged in:", user)  # Debug statement
            return Response({"message": "Login successful!", "redirect": "/home"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


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