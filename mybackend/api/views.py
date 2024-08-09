from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class SimpleAPIView(APIView):
    def get(self, request):
        return Response({"message": "Hello from Django!"})

class SignupAPIView(APIView):
    def post(self, request):
        return Response({"message": "Signup successful!"})