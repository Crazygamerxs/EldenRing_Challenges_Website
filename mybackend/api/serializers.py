# serializers.py

from rest_framework import serializers
from .models import User, Challenge, Challenge_Category, ChallengeDetail, Submission, DiscussionThread, Comment, Like, Leaderboard, Badge, UserBadge, ForumCategory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'name', 'difficulty', 'details', 'category']

class ChallengeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge_Category
        fields = ['id', 'name']


class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeDetail
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  
    class Meta:
        model = Submission
        fields = ['id', 'user', 'username', 'challenge', 'file_url', 'submitted_at', 'time_taken']  

class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = ['id', 'name']

class DiscussionThreadSerializer(serializers.ModelSerializer):
    category = ForumCategorySerializer()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = DiscussionThread
        fields = ['id', 'title', 'body', 'created_at', 'username', 'category']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

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
