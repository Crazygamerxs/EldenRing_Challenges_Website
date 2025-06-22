# Updated mybackend/urls.py

"""
Clean URL configuration for Django + React - Production Ready
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponse

# Import all your API views
from api.views import *
from api.views_health import *
from api.views_leaderboard import *
from api.views_admin import *
from api.views_notifications import *
from api.views_profile import *

# Simple debug view for testing
def debug_view(request):
    return HttpResponse(
        "<h1>Django is working!</h1>"
        "<p>React app integration test</p>"
        "<p>Visit /api/health/ to test API</p>"
    )

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # Debug endpoint
    path('debug/', debug_view),
    
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
    path('api/admin/challenges/<int:challenge_id>/', AdminChallengeDetailView.as_view()),
    path('api/admin/users/', AdminUsersView.as_view()),
    path('api/admin/users/<int:user_id>/', AdminUserDetailView.as_view()),
    path('api/admin/users/<int:user_id>/status/', AdminUserStatusView.as_view()),
    path('api/admin/categories/', AdminCategoriesView.as_view()),
    path('api/admin/recent-submissions/', AdminRecentSubmissionsView.as_view()),
    path('api/admin/settings/', AdminSettingsView.as_view()),
    
    # Notifications
    path('api/notifications/', NotificationsView.as_view()),
    path('api/notifications/<int:notification_id>/read/', MarkNotificationReadView.as_view()),
    path('api/notifications/unread-count/', UnreadNotificationsCountView.as_view()),
    
    # Health check
    path('api/health/', HealthCheckView.as_view()),

    path('db-test/', db_test_view, name='db_test'),

]

# React app catch-all with error handling
class SafeReactView(TemplateView):
    template_name = 'index.html'
    
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            # Log the error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error serving React app: {e}")
            
            # Return a simple fallback
            return HttpResponse(
                "<!DOCTYPE html>"
                "<html><head><title>Loading...</title></head>"
                "<body><h1>Application Loading</h1>"
                "<p>Please wait while the application loads...</p>"
                "<script>setTimeout(() => location.reload(), 3000);</script>"
                "</body></html>",
                content_type='text/html'
            )

# IMPORTANT: React app catch-all (must be LAST)
urlpatterns += [
    re_path(r'^.*$', SafeReactView.as_view()),
]
