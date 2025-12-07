#!/usr/bin/env python
"""
Script to create comprehensive test data for MMU Bicycle Rental System
Run with: python manage.py shell < create_test_data.py
Or: python create_test_data.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.stations.models import Station
from apps.bicycles.models import Bicycle, MaintenanceLog
from apps.rentals.models import Reservation, Rental
from apps.payments.models import Payment

User = get_user_model()

def create_test_data():
    """Create comprehensive test data"""
    
    print("🚲 Creating MMU Bicycle Rental Test Data...")
    print("=" * 50)
    
    # 1. Create Stations
    print("\n📍 Creating Stations...")
    stations_data = [
        {
            'name': 'Main Library Station',
            'code': 'LIB',
            'description': 'Located at the main university library entrance',
            'address': 'MMU Main Library, Rift Valley Rd, Nairobi',
            'latitude': -1.2245,
            'longitude': 36.8874,
            'capacity': 15,
            'operating_hours': '6:00 AM - 10:00 PM'
        },
        {
            'name': 'Engineering Block Station',
            'code': 'ENG',
            'description': 'Near the Engineering and Technology building',
            'address': 'MMU Engineering Block, Rift Valley Rd, Nairobi',
            'latitude': -1.2250,
            'longitude': 36.8880,
            'capacity': 12,
            'operating_hours': '6:00 AM - 10:00 PM'
        },
        {
            'name': 'Student Center Station',
            'code': 'SC',
            'description': 'At the student center near the cafeteria',
            'address': 'MMU Student Center, Rift Valley Rd, Nairobi',
            'latitude': -1.2240,
            'longitude': 36.8870,
            'capacity': 20,
            'operating_hours': '24/7'
        },
        {
            'name': 'Hostels Station',
            'code': 'HOST',
            'description': 'Near student hostels area',
            'address': 'MMU Hostels, Rift Valley Rd, Nairobi',
            'latitude': -1.2235,
            'longitude': 36.8865,
            'capacity': 10,
            'operating_hours': '24/7'
        }
    ]
    
    stations = []
    for data in stations_data:
        station, created = Station.objects.get_or_create(
            code=data['code'],
            defaults=data
        )
        stations.append(station)
        print(f"  {'✅ Created' if created else '⚠️  Already exists'}: {station.name}")
    
    # 2. Create Users
    print("\n👥 Creating Users...")
    users_data = [
        {
            'username': 'john_student',
            'email': 'john.kamau@students.mmu.ac.ke',
            'first_name': 'John',
            'last_name': 'Kamau',
            'password': 'password123',
            'role': 'student',
            'university_id': 'STU/12345',
            'phone_number': '+254712345678',
            'is_verified': True,
            'is_active_renter': True
        },
        {
            'username': 'mary_student',
            'email': 'mary.wanjiku@students.mmu.ac.ke',
            'first_name': 'Mary',
            'last_name': 'Wanjiku',
            'password': 'password123',
            'role': 'student',
            'university_id': 'STU/12346',
            'phone_number': '+254723456789',
            'is_verified': True,
            'is_active_renter': True
        },
        {
            'username': 'dr_omondi',
            'email': 'd.omondi@mmu.ac.ke',
            'first_name': 'David',
            'last_name': 'Omondi',
            'password': 'password123',
            'role': 'staff',
            'university_id': 'STF/67890',
            'phone_number': '+254734567890',
            'is_verified': True,
            'is_active_renter': True
        },
        {
            'username': 'peter_pending',
            'email': 'peter.mwangi@students.mmu.ac.ke',
            'first_name': 'Peter',
            'last_name': 'Mwangi',
            'password': 'password123',
            'role': 'student',
            'university_id': 'STU/12347',
            'phone_number': '+254745678901',
            'is_verified': False,
            'is_active_renter': False
        },
        {
            'username': 'jane_staff',
            'email': 'j.achieng@mmu.ac.ke',
            'first_name': 'Jane',
            'last_name': 'Achieng',
            'password': 'password123',
            'role': 'staff',
            'university_id': 'STF/67891',
            'phone_number': '+254756789012',
            'is_verified': True,
            'is_active_renter': True
        }
    ]
    
    users = []
    for data in users_data:
        password = data.pop('password')
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults=data
        )
        if created:
            user.set_password(password)
            user.save()
        users.append(user)
        print(f"  {'✅ Created' if created else '⚠️  Already exists'}: {user.username} ({user.get_role_display()})")
    
    # 3. Create Bicycles
    print("\n🚴 Creating Bicycles...")
    bicycles_data = [
        {
            'name': 'Mountain Cruiser Pro',
            'model': 'Trek X-Caliber 8',
            'manufacturer': 'Trek',
            'serial_number': 'TRK2024001',
            'description': 'High-performance mountain bike perfect for campus trails',
            'frame_size': 'M',
            'color': 'Red',
            'gear_count': 21,
            'hourly_rate': 50.00,
            'status': 'available',
            'condition': 'excellent',
            'current_station': stations[0],
            'purchase_price': 45000.00
        },
        {
            'name': 'City Comfort Bike',
            'model': 'Giant Escape 3',
            'manufacturer': 'Giant',
            'serial_number': 'GNT2024002',
            'description': 'Comfortable city bike for smooth campus rides',
            'frame_size': 'L',
            'color': 'Blue',
            'gear_count': 7,
            'hourly_rate': 40.00,
            'status': 'available',
            'condition': 'good',
            'current_station': stations[0],
            'purchase_price': 35000.00
        },
        {
            'name': 'Speed Racer',
            'model': 'Specialized Allez',
            'manufacturer': 'Specialized',
            'serial_number': 'SPC2024003',
            'description': 'Fast road bike for quick campus commutes',
            'frame_size': 'M',
            'color': 'Black',
            'gear_count': 18,
            'hourly_rate': 60.00,
            'status': 'available',
            'condition': 'excellent',
            'current_station': stations[1],
            'purchase_price': 55000.00
        },
        {
            'name': 'Campus Cruiser',
            'model': 'Schwinn Discover',
            'manufacturer': 'Schwinn',
            'serial_number': 'SCH2024004',
            'description': 'Classic cruiser perfect for leisurely campus rides',
            'frame_size': 'M',
            'color': 'Green',
            'gear_count': 7,
            'hourly_rate': 35.00,
            'status': 'available',
            'condition': 'good',
            'current_station': stations[1],
            'purchase_price': 28000.00
        },
        {
            'name': 'Trail Blazer',
            'model': 'Cannondale Trail 5',
            'manufacturer': 'Cannondale',
            'serial_number': 'CND2024005',
            'description': 'Versatile mountain bike for all terrains',
            'frame_size': 'L',
            'color': 'Orange',
            'gear_count': 24,
            'hourly_rate': 55.00,
            'status': 'available',
            'condition': 'excellent',
            'current_station': stations[2],
            'purchase_price': 48000.00
        },
        {
            'name': 'Urban Explorer',
            'model': 'Trek FX 2',
            'manufacturer': 'Trek',
            'serial_number': 'TRK2024006',
            'description': 'Hybrid bike perfect for campus and city riding',
            'frame_size': 'M',
            'color': 'Silver',
            'gear_count': 9,
            'hourly_rate': 45.00,
            'status': 'available',
            'condition': 'good',
            'current_station': stations[2],
            'purchase_price': 38000.00
        },
        {
            'name': 'Easy Rider',
            'model': 'Giant Sedona DX',
            'manufacturer': 'Giant',
            'serial_number': 'GNT2024007',
            'description': 'Comfortable bike for relaxed campus touring',
            'frame_size': 'L',
            'color': 'Brown',
            'gear_count': 21,
            'hourly_rate': 40.00,
            'status': 'available',
            'condition': 'fair',
            'current_station': stations[3],
            'purchase_price': 32000.00
        },
        {
            'name': 'Quick Commuter',
            'model': 'Raleigh Cadent 2',
            'manufacturer': 'Raleigh',
            'serial_number': 'RAL2024008',
            'description': 'Fast and efficient for daily commutes',
            'frame_size': 'M',
            'color': 'White',
            'gear_count': 16,
            'hourly_rate': 50.00,
            'status': 'maintenance',
            'condition': 'good',
            'current_station': stations[3],
            'purchase_price': 40000.00
        },
        {
            'name': 'Campus Classic',
            'model': 'Schwinn Wayfarer',
            'manufacturer': 'Schwinn',
            'serial_number': 'SCH2024009',
            'description': 'Retro-style bike with modern features',
            'frame_size': 'M',
            'color': 'Cream',
            'gear_count': 7,
            'hourly_rate': 45.00,
            'status': 'available',
            'condition': 'excellent',
            'current_station': stations[0],
            'purchase_price': 36000.00
        },
        {
            'name': 'Sport Tourer',
            'model': 'Trek Domane AL 2',
            'manufacturer': 'Trek',
            'serial_number': 'TRK2024010',
            'description': 'Sporty touring bike for longer rides',
            'frame_size': 'L',
            'color': 'Navy Blue',
            'gear_count': 16,
            'hourly_rate': 55.00,
            'status': 'available',
            'condition': 'excellent',
            'current_station': stations[1],
            'purchase_price': 50000.00
        }
    ]
    
    bicycles = []
    for data in bicycles_data:
        bicycle, created = Bicycle.objects.get_or_create(
            serial_number=data['serial_number'],
            defaults=data
        )
        bicycles.append(bicycle)
        print(f"  {'✅ Created' if created else '⚠️  Already exists'}: {bicycle.name} ({bicycle.serial_number})")
    
    # 4. Create Sample Completed Rentals
    print("\n📋 Creating Sample Completed Rentals...")
    completed_rentals_data = [
        {
            'user': users[0],  # john_student
            'bicycle': bicycles[0],
            'pickup_station': stations[0],
            'return_station': stations[1],
            'start_time': timezone.now() - timedelta(days=5, hours=2),
            'end_time': timezone.now() - timedelta(days=5),
            'status': 'completed',
            'distance_km': 8.5,
            'pickup_notes': 'Bike in excellent condition',
            'return_notes': 'No issues, smooth ride'
        },
        {
            'user': users[1],  # mary_student
            'bicycle': bicycles[1],
            'pickup_station': stations[1],
            'return_station': stations[2],
            'start_time': timezone.now() - timedelta(days=3, hours=1),
            'end_time': timezone.now() - timedelta(days=3),
            'status': 'completed',
            'distance_km': 5.2,
            'pickup_notes': 'Good condition',
            'return_notes': 'All good'
        },
        {
            'user': users[0],  # john_student
            'bicycle': bicycles[2],
            'pickup_station': stations[0],
            'return_station': stations[0],
            'start_time': timezone.now() - timedelta(days=1, hours=3),
            'end_time': timezone.now() - timedelta(days=1),
            'status': 'completed',
            'distance_km': 12.3,
            'pickup_notes': 'Perfect condition',
            'return_notes': 'Great bike!'
        }
    ]
    
    for data in completed_rentals_data:
        rental = Rental.objects.create(**data)
        rental.calculate_cost()
        rental.save()
        print(f"  ✅ Created rental: {rental.user.username} - {rental.bicycle.name}")
    
    # 5. Create Sample Maintenance Log
    print("\n🔧 Creating Maintenance Logs...")
    if bicycles[7].status == 'maintenance':
        maintenance = MaintenanceLog.objects.create(
            bicycle=bicycles[7],
            description='Brake pad replacement and gear adjustment',
            cost=1500.00,
            performed_by='Tech Team',
            is_completed=False
        )
        print(f"  ✅ Created maintenance log for {bicycles[7].name}")
    
    print("\n" + "=" * 50)
    print("✅ Test data creation completed!")
    print("\n📊 Summary:")
    print(f"  Stations: {Station.objects.count()}")
    print(f"  Users: {User.objects.count()}")
    print(f"  Bicycles: {Bicycle.objects.count()}")
    print(f"  Completed Rentals: {Rental.objects.filter(status='completed').count()}")
    print(f"  Maintenance Logs: {MaintenanceLog.objects.count()}")
    print("\n🔑 Test User Credentials:")
    print("  Username: john_student | Password: password123")
    print("  Username: mary_student | Password: password123")
    print("  Username: dr_omondi | Password: password123")
    print("  Username: peter_pending | Password: password123 (not verified)")
    print("\n🚀 You can now login and test the system!")


if __name__ == '__main__':
    create_test_data()