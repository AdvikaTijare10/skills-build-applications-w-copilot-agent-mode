from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
        ]
        teams = [
            {"name": "marvel", "members": ["ironman@marvel.com", "cap@marvel.com"]},
            {"name": "dc", "members": ["batman@dc.com", "wonderwoman@dc.com"]},
        ]
        activities = [
            {"user_email": "ironman@marvel.com", "activity": "Running", "duration": 30},
            {"user_email": "cap@marvel.com", "activity": "Cycling", "duration": 45},
            {"user_email": "batman@dc.com", "activity": "Swimming", "duration": 60},
            {"user_email": "wonderwoman@dc.com", "activity": "Yoga", "duration": 40},
        ]
        leaderboard = [
            {"team": "marvel", "points": 150},
            {"team": "dc", "points": 140},
        ]
        workouts = [
            {"user_email": "ironman@marvel.com", "workout": "Pushups", "reps": 50},
            {"user_email": "cap@marvel.com", "workout": "Situps", "reps": 60},
            {"user_email": "batman@dc.com", "workout": "Pullups", "reps": 30},
            {"user_email": "wonderwoman@dc.com", "workout": "Squats", "reps": 70},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
