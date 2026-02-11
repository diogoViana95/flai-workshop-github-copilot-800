from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpass123',
            'team': 'Test Team'
        }
    
    def test_create_user(self):
        response = self.client.post('/api/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
    
    def test_get_users(self):
        User.objects.create(**self.user_data)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TeamAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            'name': 'Test Team',
            'description': 'A test team',
            'members': []
        }
    
    def test_create_team(self):
        response = self.client.post('/api/teams/', self.team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get().name, 'Test Team')
    
    def test_get_teams(self):
        Team.objects.create(**self.team_data)
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ActivityAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'user_email': 'test@example.com',
            'activity_type': 'Running',
            'duration': 30,
            'calories': 300,
            'distance': 5.0,
            'date': datetime.now(),
            'notes': 'Morning run'
        }
    
    def test_create_activity(self):
        response = self.client.post('/api/activities/', self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        self.assertEqual(Activity.objects.get().activity_type, 'Running')
    
    def test_get_activities(self):
        Activity.objects.create(**self.activity_data)
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class LeaderboardAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.leaderboard_data = {
            'user_email': 'test@example.com',
            'team': 'Test Team',
            'total_calories': 1000,
            'total_activities': 5,
            'total_duration': 150,
            'rank': 1
        }
    
    def test_create_leaderboard_entry(self):
        response = self.client.post('/api/leaderboard/', self.leaderboard_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Leaderboard.objects.count(), 1)
        self.assertEqual(Leaderboard.objects.get().rank, 1)
    
    def test_get_leaderboard(self):
        Leaderboard.objects.create(**self.leaderboard_data)
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class WorkoutAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.workout_data = {
            'name': 'Morning HIIT',
            'description': 'High intensity interval training',
            'activity_type': 'HIIT',
            'difficulty': 'Hard',
            'duration': 30,
            'calories_estimate': 400,
            'exercises': [
                {'name': 'Burpees', 'sets': 3, 'reps': 10},
                {'name': 'Jump Squats', 'sets': 3, 'reps': 15}
            ]
        }
    
    def test_create_workout(self):
        response = self.client.post('/api/workouts/', self.workout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)
        self.assertEqual(Workout.objects.get().name, 'Morning HIIT')
    
    def test_get_workouts(self):
        Workout.objects.create(**self.workout_data)
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filter_by_difficulty(self):
        Workout.objects.create(**self.workout_data)
        response = self.client.get('/api/workouts/by_difficulty/?difficulty=Hard')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
