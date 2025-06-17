"""
Clean URL configuration for Django + React
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Import all your API views
from api.views import *
from api.views_health import *
from api.views_leaderboard import *
from api.views_admin import *
from api.views_notifications import *
from api.views_profile import *

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', SimpleAPIView.as_view()),
    path('api/csrf-token/', GETCSRFToken.as_view()),
    
    # Auth
    path('api/signup/', SignupAPIView.as_view()),
    path('api/login/', LoginAPIView.as_view()),
    path('api/logout/', LogoutAPIView.as_view()),
    path('api/user-profile/', UserProfileAPIView.as_view()),
    
    # Challenges
    path('api/challenge/', ChallengeAPIView.as_view()),
    path('api/challenge/<int:challenge_id>/', ChallengeAPIView.as_view()),
    path('api/submissions/', ChallengeSubmissionsView.as_view()),
    path('api/submit_run/', SubmitRunAPIView.as_view()),
    
    # Leaderboard
    path('api/leaderboard/challenges/', LeaderboardChallengesView.as_view()),
    path('api/leaderboard/points/', LeaderboardPointsView.as_view()),
    
    # Admin
    path('api/admin/stats/', AdminStatsView.as_view()),
    path('api/admin/submissions/', AdminSubmissionsView.as_view()),
    path('api/admin/submissions/<int:submission_id>/approve/', AdminApproveSubmissionView.as_view()),
    path('api/admin/submissions/<int:submission_id>/reject/', AdminRejectSubmissionView.as_view()),
    path('api/admin/challenges/', AdminChallengesView.as_view()),
    path('api/admin/users/', AdminUsersView.as_view()),
    path('api/admin/settings/', AdminSettingsView.as_view()),
    
    # Notifications
    path('api/notifications/', NotificationsView.as_view()),
    path('api/notifications/<int:notification_id>/read/', MarkNotificationReadView.as_view()),
    path('api/notifications/unread-count/', UnreadNotificationsCountView.as_view()),
    
    # Health check
    path('api/health/', HealthCheckView.as_view()),
]

# Serve static files - CORRECTED SYNTAX
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, settings.STATIC_ROOT)

# IMPORTANT: React app catch-all (must be LAST)
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]