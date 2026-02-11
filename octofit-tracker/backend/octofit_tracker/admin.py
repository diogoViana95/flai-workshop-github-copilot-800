from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('_id', 'name', 'email', 'team', 'created_at')
    list_filter = ('team', 'created_at')
    search_fields = ('name', 'email', 'team')
    readonly_fields = ('_id', 'created_at')
    fields = ('name', 'email', 'password', 'team', 'created_at')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('_id', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('_id', 'created_at')
    fields = ('name', 'description', 'members', 'created_at')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('_id', 'user_email', 'activity_type', 'duration', 'calories', 'date')
    list_filter = ('activity_type', 'date')
    search_fields = ('user_email', 'activity_type', 'notes')
    readonly_fields = ('_id',)
    fields = ('user_email', 'activity_type', 'duration', 'calories', 'distance', 'date', 'notes')
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('_id', 'user_email', 'team', 'rank', 'total_calories', 'total_activities', 'total_duration', 'updated_at')
    list_filter = ('team', 'rank', 'updated_at')
    search_fields = ('user_email', 'team')
    readonly_fields = ('_id', 'updated_at')
    fields = ('user_email', 'team', 'total_calories', 'total_activities', 'total_duration', 'rank', 'updated_at')
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('_id', 'name', 'activity_type', 'difficulty', 'duration', 'calories_estimate')
    list_filter = ('activity_type', 'difficulty')
    search_fields = ('name', 'description', 'activity_type')
    readonly_fields = ('_id',)
    fields = ('name', 'description', 'activity_type', 'difficulty', 'duration', 'calories_estimate', 'exercises')
