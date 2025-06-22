from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Challenge, Challenge_Category, Submission, 
    Notification, SiteSettings
)

# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'total_points', 'challenges_completed_count', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-total_points', 'username')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('total_points', 'challenges_completed_count')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

# Challenge Category Admin
@admin.register(Challenge_Category)
class ChallengeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'challenge_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def challenge_count(self, obj):
        return Challenge.objects.filter(category=obj).count()
    challenge_count.short_description = 'Challenges'

# Challenge Admin
@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'difficulty', 'base_points', 'total_points', 'is_dlc', 'is_combination', 'completion_count')
    list_filter = ('category', 'difficulty', 'is_dlc', 'is_combination')
    search_fields = ('name', 'details')
    ordering = ('category', 'difficulty', 'name')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'details', 'category', 'difficulty')
        }),
        ('Points & Modifiers', {
            'fields': ('base_points', 'is_dlc', 'is_combination'),
            'description': 'Base points are auto-calculated. DLC adds +5 points, Combination adds +10 points.'
        }),
    )
    
    readonly_fields = ('base_points',)
    
    def total_points(self, obj):
        return obj.get_total_points()
    total_points.short_description = 'Total Points'
    
    def completion_count(self, obj):
        return Submission.objects.filter(challenge=obj, status='approved').count()
    completion_count.short_description = 'Completions'

# Submission Admin
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'challenge', 'status', 'points_awarded', 'submitted_at', 'approved_at', 'approved_by')
    list_filter = ('status', 'submitted_at', 'approved_at', 'challenge__category', 'challenge__difficulty')
    search_fields = ('user__username', 'challenge__name')
    ordering = ('-submitted_at',)
    
    fieldsets = (
        ('Submission Info', {
            'fields': ('user', 'challenge', 'file_url', 'time_taken', 'admin_verified_time')
        }),
        ('Status & Points', {
            'fields': ('status', 'points_awarded', 'reject_reason')
        }),
        ('Approval Info', {
            'fields': ('approved_at', 'approved_by'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('submitted_at', 'approved_at')
    
    actions = ['approve_submissions', 'reject_submissions']
    
    def approve_submissions(self, request, queryset):
        for submission in queryset:
            if submission.status != 'approved':
                submission.status = 'approved'
                submission.points_awarded = submission.challenge.get_total_points()
                submission.approved_by = request.user
                submission.save()
                submission.user.update_points_and_challenges()
        self.message_user(request, f'{queryset.count()} submissions approved.')
    approve_submissions.short_description = 'Approve selected submissions'
    
    def reject_submissions(self, request, queryset):
        for submission in queryset:
            if submission.status != 'rejected':
                submission.status = 'rejected'
                submission.points_awarded = 0
                submission.approved_by = None
                submission.save()
                submission.user.update_points_and_challenges()
        self.message_user(request, f'{queryset.count()} submissions rejected.')
    reject_submissions.short_description = 'Reject selected submissions'

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'type', 'status', 'read', 'created_at')
    list_filter = ('type', 'status', 'read', 'created_at')
    search_fields = ('user__username', 'title', 'content')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Notification Info', {
            'fields': ('user', 'title', 'content', 'type')
        }),
        ('Status & Links', {
            'fields': ('status', 'read', 'challenge')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)

# Site Settings Admin
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'enable_registrations', 'enable_submissions', 'maintenance_mode', 'max_submissions_per_day')
    
    fieldsets = (
        ('Site Configuration', {
            'fields': ('site_name', 'site_description', 'notification_email')
        }),
        ('Feature Toggles', {
            'fields': ('enable_registrations', 'enable_submissions', 'maintenance_mode', 'auto_approve_submissions')
        }),
        ('Limits', {
            'fields': ('max_submissions_per_day',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one SiteSettings instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of SiteSettings
        return False

# Customize admin site headers
admin.site.site_header = "Elden Ring Challenges Admin"
admin.site.site_title = "Elden Ring Admin"
admin.site.index_title = "Welcome to Elden Ring Challenges Administration"
