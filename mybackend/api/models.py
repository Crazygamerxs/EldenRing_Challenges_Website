from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import timedelta

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    
    # Points system
    total_points = models.IntegerField(default=0)
    challenges_completed_count = models.IntegerField(default=0)

    # Required fields for Django admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def update_points_and_challenges(self):
        """Update user's total points and challenge count based on approved submissions"""
        approved_submissions = Submission.objects.filter(user=self, status='approved')
        self.total_points = sum(sub.points_awarded for sub in approved_submissions if sub.points_awarded)
        self.challenges_completed_count = approved_submissions.count()
        self.save()

    def __str__(self):
        return self.email

class Challenge_Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Challenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
        ('Extreme', 'Extreme'),
    ]

    name = models.CharField(max_length=255)
    details = models.TextField()
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES)
    category = models.ForeignKey(Challenge_Category, on_delete=models.CASCADE)
    
    # Challenge type fields
    is_dlc = models.BooleanField(default=False, help_text="True if this challenge requires DLC content")
    is_combination = models.BooleanField(default=False, help_text="True if this challenge combines multiple challenges")
    
    # Points system
    base_points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.base_points == 0:  # Only calculate if not set
            self.base_points = self.calculate_base_points()
        super().save(*args, **kwargs)

    def calculate_base_points(self):
        """Calculate base points based on difficulty"""
        difficulty_points = {
            'Easy': 50,
            'Medium': 100,
            'Hard': 200,
            'Extreme': 500,
        }
        return difficulty_points.get(self.difficulty, 50)

    def get_total_points(self):
        """Get total points including bonuses"""
        points = self.base_points
        
        # DLC bonus
        if self.is_dlc:
            points += 25
        
        # Combination challenge bonus
        if self.is_combination:
            points += 50
        
        return points
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['category', 'name']

class ChallengeDetail(models.Model):
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Detail for {self.submission.challenge.name}"

class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    file_url = models.URLField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.DurationField(default=timedelta())
    admin_verified_time = models.DurationField(null=True, blank=True)  # ADD THIS LINE
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reject_reason = models.TextField(blank=True, null=True)
    
    # Points tracking
    points_awarded = models.IntegerField(default=0)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_submissions')

    def format_time(self):
        """Format duration as HH:MM:SS"""
        total_seconds = int(self.time_taken.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def format_admin_time(self):  # ADD THIS METHOD
        """Format admin verified time as HH:MM:SS"""
        if not self.admin_verified_time:
            return None
        total_seconds = int(self.admin_verified_time.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def remove_points(self):
        """Remove points when submission is rejected after being approved"""
        if self.points_awarded > 0:
            self.points_awarded = 0
            self.user.update_points_and_challenges()

    def __str__(self):
        return f"Submission by {self.user.email} for {self.challenge.name}"
class ForumCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class DiscussionThread(models.Model):
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.thread.title}"

class Like(models.Model):
    post_id = models.PositiveIntegerField()  # To track likes on threads and comments
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Like by {self.user.email} on post {self.post_id}"

class Leaderboard(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_taken = models.DurationField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leaderboard entry for {self.challenge.name} by {self.user.email}"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} has badge {self.badge.name}"

class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Not Completed', 'Not Completed'), ('Completed', 'Completed')])
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User {self.user.email} - Challenge {self.challenge.name} - Status {self.status}"

class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('error', 'Error'),
        ('warning', 'Warning'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

class SiteSettings(models.Model):
    """Site-wide settings model"""
    site_name = models.CharField(max_length=100, default='Elden Ring Challenges')
    site_description = models.TextField(default='A platform for Elden Ring challenge runs')
    enable_registrations = models.BooleanField(default=True)
    enable_submissions = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    notification_email = models.EmailField(default='admin@eldenring.com')
    max_submissions_per_day = models.IntegerField(default=5)
    auto_approve_submissions = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    @classmethod
    def get_settings(cls):
        """Get or create the site settings instance"""
        settings, created = cls.objects.get_or_create(pk=1)
        if created:
            print("Created new SiteSettings instance with default values")
        return settings
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Prevent deletion of settings
        pass
    
    def __str__(self):
        return f"Site Settings - {self.site_name}"