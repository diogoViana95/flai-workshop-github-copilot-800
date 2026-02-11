from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data using Django ORM
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes fighting for fitness',
            members=[]
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League champions of wellness',
            members=[]
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create Marvel Users
        self.stdout.write('Creating Marvel superheroes...')
        marvel_users = [
            User.objects.create(
                name='Tony Stark',
                email='ironman@marvel.com',
                password='arc_reactor_3000',
                team='Team Marvel'
            ),
            User.objects.create(
                name='Steve Rogers',
                email='captain@marvel.com',
                password='shield_throw_99',
                team='Team Marvel'
            ),
            User.objects.create(
                name='Natasha Romanoff',
                email='blackwidow@marvel.com',
                password='red_in_ledger',
                team='Team Marvel'
            ),
            User.objects.create(
                name='Bruce Banner',
                email='hulk@marvel.com',
                password='angry_science',
                team='Team Marvel'
            ),
            User.objects.create(
                name='Thor Odinson',
                email='thor@marvel.com',
                password='worthiness_check',
                team='Team Marvel'
            ),
        ]
        
        # Create DC Users
        self.stdout.write('Creating DC superheroes...')
        dc_users = [
            User.objects.create(
                name='Clark Kent',
                email='superman@dc.com',
                password='kryptonite_fear',
                team='Team DC'
            ),
            User.objects.create(
                name='Bruce Wayne',
                email='batman@dc.com',
                password='im_batman',
                team='Team DC'
            ),
            User.objects.create(
                name='Diana Prince',
                email='wonderwoman@dc.com',
                password='lasso_truth',
                team='Team DC'
            ),
            User.objects.create(
                name='Barry Allen',
                email='flash@dc.com',
                password='speed_force',
                team='Team DC'
            ),
            User.objects.create(
                name='Arthur Curry',
                email='aquaman@dc.com',
                password='ocean_king',
                team='Team DC'
            ),
        ]
        
        all_users = marvel_users + dc_users
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_users)} superheroes'))
        
        # Update team members
        team_marvel.members = [u.email for u in marvel_users]
        team_marvel.save()
        team_dc.members = [u.email for u in dc_users]
        team_dc.save()
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Swimming', 'Cycling', 'Weight Training', 'Yoga', 'Boxing', 'HIIT']
        activities_created = 0
        
        for user in all_users:
            for i in range(5):
                import random
                activity_type = random.choice(activity_types)
                duration = random.randint(30, 120)
                calories = duration * random.randint(5, 12)
                distance = round(random.uniform(3, 15), 2) if activity_type in ['Running', 'Swimming', 'Cycling'] else None
                
                Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type,
                    duration=duration,
                    calories=calories,
                    distance=distance,
                    date=timezone.now() - timedelta(days=random.randint(0, 30)),
                    notes=f'{user.name} crushing it with {activity_type}!'
                )
                activities_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activities_created} activities'))
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard...')
        leaderboard_data = []
        
        for user in all_users:
            user_activities = Activity.objects.filter(user_email=user.email)
            total_calories = sum(a.calories for a in user_activities)
            total_duration = sum(a.duration for a in user_activities)
            total_activities_count = user_activities.count()
            
            leaderboard_data.append({
                'user': user,
                'total_calories': total_calories,
                'total_duration': total_duration,
                'total_activities': total_activities_count
            })
        
        # Sort by total calories to assign rank
        leaderboard_data.sort(key=lambda x: x['total_calories'], reverse=True)
        
        for rank, data in enumerate(leaderboard_data, start=1):
            Leaderboard.objects.create(
                user_email=data['user'].email,
                team=data['user'].team,
                total_calories=data['total_calories'],
                total_activities=data['total_activities'],
                total_duration=data['total_duration'],
                rank=rank
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_data)} leaderboard entries'))
        
        # Create Workouts
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            Workout.objects.create(
                name='Iron Man Suit Training',
                description='High-intensity workout to build endurance like Tony Stark',
                activity_type='HIIT',
                difficulty='Hard',
                duration=45,
                calories_estimate=600,
                exercises=[
                    {'name': 'Burpees', 'reps': 20, 'sets': 4},
                    {'name': 'Mountain Climbers', 'reps': 30, 'sets': 4},
                    {'name': 'Jump Squats', 'reps': 15, 'sets': 4}
                ]
            ),
            Workout.objects.create(
                name='Captain America Shield Drill',
                description='Build super soldier strength and agility',
                activity_type='Weight Training',
                difficulty='Hard',
                duration=60,
                calories_estimate=500,
                exercises=[
                    {'name': 'Bench Press', 'reps': 10, 'sets': 4},
                    {'name': 'Pull-ups', 'reps': 12, 'sets': 4},
                    {'name': 'Deadlifts', 'reps': 8, 'sets': 4}
                ]
            ),
            Workout.objects.create(
                name='Black Widow Flexibility Flow',
                description='Enhance flexibility and balance like Natasha',
                activity_type='Yoga',
                difficulty='Medium',
                duration=45,
                calories_estimate=250,
                exercises=[
                    {'name': 'Warrior Pose', 'duration': '2 minutes', 'sets': 3},
                    {'name': 'Tree Pose', 'duration': '1 minute', 'sets': 3},
                    {'name': 'Downward Dog', 'duration': '3 minutes', 'sets': 3}
                ]
            ),
            Workout.objects.create(
                name='Flash Speed Training',
                description='Speed and cardio workout inspired by the Scarlet Speedster',
                activity_type='Running',
                difficulty='Hard',
                duration=40,
                calories_estimate=550,
                exercises=[
                    {'name': 'Sprint Intervals', 'duration': '30 seconds', 'sets': 10},
                    {'name': 'High Knees', 'reps': 50, 'sets': 5},
                    {'name': 'Shuttle Runs', 'duration': '1 minute', 'sets': 5}
                ]
            ),
            Workout.objects.create(
                name='Wonder Woman Warrior Training',
                description='Full-body strength and power workout',
                activity_type='Weight Training',
                difficulty='Hard',
                duration=55,
                calories_estimate=520,
                exercises=[
                    {'name': 'Overhead Press', 'reps': 10, 'sets': 4},
                    {'name': 'Lunges', 'reps': 15, 'sets': 4},
                    {'name': 'Battle Ropes', 'duration': '1 minute', 'sets': 4}
                ]
            ),
            Workout.objects.create(
                name='Aquaman Ocean Swim',
                description='Swimming workout fit for the King of Atlantis',
                activity_type='Swimming',
                difficulty='Medium',
                duration=50,
                calories_estimate=450,
                exercises=[
                    {'name': 'Freestyle', 'distance': '500m', 'sets': 4},
                    {'name': 'Butterfly Stroke', 'distance': '200m', 'sets': 3},
                    {'name': 'Treading Water', 'duration': '5 minutes', 'sets': 2}
                ]
            ),
            Workout.objects.create(
                name='Batman Combat Training',
                description='Mixed martial arts and boxing workout',
                activity_type='Boxing',
                difficulty='Hard',
                duration=50,
                calories_estimate=580,
                exercises=[
                    {'name': 'Heavy Bag', 'duration': '3 minutes', 'sets': 5},
                    {'name': 'Speed Bag', 'duration': '2 minutes', 'sets': 5},
                    {'name': 'Shadow Boxing', 'duration': '3 minutes', 'sets': 4}
                ]
            ),
            Workout.objects.create(
                name='Beginner Hero Foundation',
                description='Start your superhero fitness journey',
                activity_type='Weight Training',
                difficulty='Easy',
                duration=30,
                calories_estimate=250,
                exercises=[
                    {'name': 'Bodyweight Squats', 'reps': 15, 'sets': 3},
                    {'name': 'Push-ups', 'reps': 10, 'sets': 3},
                    {'name': 'Planks', 'duration': '30 seconds', 'sets': 3}
                ]
            ),
        ]
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workout suggestions'))
        
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write(f'Total Users: {User.objects.count()}')
        self.stdout.write(f'Total Teams: {Team.objects.count()}')
        self.stdout.write(f'Total Activities: {Activity.objects.count()}')
        self.stdout.write(f'Total Leaderboard Entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Total Workouts: {Workout.objects.count()}')
