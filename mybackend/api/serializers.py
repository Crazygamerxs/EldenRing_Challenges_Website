# serializers.py

from rest_framework import serializers
from .models import User, Challenge, Challenge_Category, ChallengeDetail, Submission, DiscussionThread, Comment, Like, Leaderboard, Badge, UserBadge, ForumCategory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    
    class Meta:
        model = Challenge
        fields = ['id', 'name', 'details', 'difficulty', 'category', 'is_dlc', 'is_combination', 'completed']
    
    def get_completed(self, obj):
        # This will be overridden by the view when user context is available
        return False
    
class ChallengeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge_Category
        fields = ['id', 'name']


class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeDetail
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    submitted_at = serializers.DateTimeField()  # Add this line if you have a submission date field in the model

    class Meta:
        model = Submission
        fields = ['file_url', 'challenge', 'user', 'username', 'time_taken', 'submitted_at']

    def get_username(self, obj):
        return obj.user.username if obj.user else None


# for the Community Form Page
class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = ['id', 'name']


# For the community thread detail page
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at', 'username']

class DiscussionThreadSerializer(serializers.ModelSerializer):
    category = ForumCategorySerializer()
    username = serializers.CharField(source='user.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = DiscussionThread
        fields = ['id', 'title', 'body', 'created_at', 'username', 'category', 'comments']



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = '__all__'

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = '__all__'
