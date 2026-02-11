from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'password', 'team', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'members', 'created_at']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['_id', 'user_email', 'activity_type', 'duration', 'calories', 'distance', 'date', 'notes']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user_email', 'team', 'total_calories', 'total_activities', 'total_duration', 'rank', 'updated_at']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'activity_type', 'difficulty', 'duration', 'calories_estimate', 'exercises']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation
