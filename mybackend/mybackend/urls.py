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
from api.views import SimpleAPIView, GETCSRFToken, SignupAPIView, LoginAPIView, LogoutAPIView, HomeAPIView, ChallengeAPIView, ChallengeDetailView, ChallengeSubmissionsView, ThreadListView, ThreadDetailView, UserProfileAPIView, SubmitRunAPIView, PasswordResetConfirmView, PasswordResetRequestView
from api.views_leaderboard import LeaderboardChallengesView, LeaderboardPointsView
from api.views_admin import (
    AdminStatsView, AdminRecentSubmissionsView, AdminSubmissionsView, 
    AdminApproveSubmissionView, AdminRejectSubmissionView, AdminChallengesView,
    AdminChallengeDetailView, AdminCategoriesView, AdminUsersView, 
    AdminUserDetailView, AdminUserStatusView, AdminSettingsView
)
from api.views_notifications import NotificationsView, MarkNotificationReadView, MarkAllNotificationsReadView, UnreadNotificationsCountView
from api.views_profile import UserProfilePlaceholder
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
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/home/', HomeAPIView.as_view(), name='home'),
    path('api/challenge/', ChallengeAPIView.as_view(), name='challenge'),
    path('api/challenge/<int:pk>/', ChallengeDetailView.as_view(), name='challenge-specific'),
    path('api/submissions/', ChallengeSubmissionsView.as_view(), name='challenge-submissions'),
    path('api/threads/', ThreadListView.as_view(), name='thread-list'),
    path('api/threads/<int:thread_id>/', ThreadDetailView.as_view(), name='thread-detail'),
    path('api/user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('api/submit_run/', SubmitRunAPIView.as_view(), name='submit-run'),
    
    # Leaderboard endpoints
    path('api/leaderboard/challenges/', LeaderboardChallengesView.as_view(), name='leaderboard-challenges'),
    path('api/leaderboard/points/', LeaderboardPointsView.as_view(), name='leaderboard-points'),
    
    # Admin endpoints
    path('api/admin/stats/', AdminStatsView.as_view(), name='admin-stats'),
    path('api/admin/submissions/recent/', AdminRecentSubmissionsView.as_view(), name='admin-recent-submissions'),
    path('api/admin/submissions/', AdminSubmissionsView.as_view(), name='admin-submissions'),
    path('api/admin/submissions/<int:submission_id>/approve/', AdminApproveSubmissionView.as_view(), name='admin-approve-submission'),
    path('api/admin/submissions/<int:submission_id>/reject/', AdminRejectSubmissionView.as_view(), name='admin-reject-submission'),
    
    # Admin challenge endpoints
    path('api/admin/challenges/', AdminChallengesView.as_view(), name='admin-challenges'),
    path('api/admin/challenges/<int:challenge_id>/', AdminChallengeDetailView.as_view(), name='admin-challenge-detail'),
    path('api/categories/', AdminCategoriesView.as_view(), name='admin-categories'),
    
    # Admin user endpoints
    path('api/admin/users/', AdminUsersView.as_view(), name='admin-users'),
    path('api/admin/users/<int:user_id>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('api/admin/users/<int:user_id>/status/', AdminUserStatusView.as_view(), name='admin-user-status'),
    
    # Admin settings endpoint
    path('api/admin/settings/', AdminSettingsView.as_view(), name='admin-settings'),
    
    # User profile endpoints (disabled)
    path('api/user-profile/<path:path>', UserProfilePlaceholder.as_view(), name='user-profile-placeholder'),
    
    # Notification endpoints
    path('api/notifications/', NotificationsView.as_view(), name='notifications'),
    path('api/notifications/<int:notification_id>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('api/notifications/mark-all-read/', MarkAllNotificationsReadView.as_view(), name='mark-all-notifications-read'),
    path('api/notifications/unread-count/', UnreadNotificationsCountView.as_view(), name='unread-notifications-count'),
    
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

# if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
