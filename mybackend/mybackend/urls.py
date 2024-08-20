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
from django.urls import path, re_path
from api.views import SimpleAPIView, GETCSRFToken, SignupAPIView, LoginAPIView, LogoutAPIView, HomeAPIView, ChallengeAPIView, ChallengeDetailView, ChallengeSubmissionsView, ThreadListView, ThreadDetailView, UserProfileAPIView, SubmitRunAPIView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', SimpleAPIView.as_view()),
    path('api/csrf-token/', GETCSRFToken.as_view(), name='csrf_token'),
    path('api/signup/', SignupAPIView.as_view(), name='signup'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/home/', HomeAPIView.as_view(), name='home'),
    path('api/challenge/', ChallengeAPIView.as_view(), name='challenge'),
    path('api/challenge/<int:pk>/', ChallengeDetailView.as_view(), name='challenge-specific'),
    path('api/submissions/', ChallengeSubmissionsView.as_view(), name='challenge-submissions'),
    path('api/threads/', ThreadListView.as_view(), name='thread-list'),
    path('api/threads/<int:thread_id>/', ThreadDetailView.as_view(), name='thread-detail'),
    path('api/user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('api/submit_run/', SubmitRunAPIView.as_view(), name='submit-run'),

    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)