from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    profile_image = models.URLField(blank=True, null=True)
    completed_challenges = models.JSONField(default=list, blank=True)  # Optional
    badges = models.JSONField(default=list, blank=True)  # Optional

    # Required fields for Django admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

class Challenge_Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Challenge(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Challenge_Category, on_delete=models.CASCADE)
    details = models.TextField()
    difficulty = models.CharField(max_length=10, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])

    def __str__(self):
        return self.name

class ChallengeDetail(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE)
    time_taken = models.DurationField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Detail for {self.challenge.name}"

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    file_url = models.URLField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user.email} for {self.challenge.name}"

class DiscussionThread(models.Model):
    category = models.CharField(max_length=20, choices=[('Introduction', 'Introduction'), ('Challenges', 'Challenges'), ('Other Talk', 'Other Talk'), ('Site', 'Site')])
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
