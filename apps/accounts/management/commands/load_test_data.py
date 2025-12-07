"""
Management command to load test data
Usage: python manage.py load_test_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.stations.models import Station
from apps.bicycles.models import Bicycle, MaintenanceLog
from apps.rentals.models import Rental

User = get_user_model()


class Command(BaseCommand):
    help = 'Load comprehensive test data for MMU Bicycle Rental System'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚲 Loading Test Data...'))
        
        # Import and run the creation script
        from create_test_data import create_test_data
        create_test_data()
        
        self.stdout.write(self.style.SUCCESS('✅ Test data loaded successfully!'))