"""
URL configuration for mybackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import SimpleAPIView, SignupAPIView, LoginAPIView, HomeAPIView, ChallengeAPIView, ChallengeDetailView, ChallengeSubmissionsView, ThreadListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', SimpleAPIView.as_view()),
    path('api/signup/', SignupAPIView.as_view(), name='signup'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/home/', HomeAPIView.as_view(), name='home'),
    path('api/challenge/', ChallengeAPIView.as_view(), name='challenge'),
    path('api/challenge/<int:pk>/', ChallengeDetailView.as_view(), name='challenge-specific'),
    path('api/submissions/', ChallengeSubmissionsView.as_view(), name='challenge-submissions'),
    path('api/threads/', ThreadListView.as_view(), name='thread-list'),
    ]
