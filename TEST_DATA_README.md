# Test Data Guide

## 🎯 Quick Start

### Option 1: Using Python Script (Recommended)
```bash
python3 create_test_data.py
```

### Option 2: Using Django Shell
```bash
python3 manage.py shell < create_test_data.py
```

---

## 📊 What Gets Created

### 1. **Stations (4)**
- Main Library Station (LIB) - 15 capacity
- Engineering Block Station (ENG) - 12 capacity
- Student Center Station (SC) - 20 capacity
- Hostels Station (HOST) - 10 capacity

### 2. **Users (5)**

| Username | Password | Role | University ID | Verified | Status |
|----------|----------|------|---------------|----------|--------|
| john_student | password123 | Student | STU/12345 | ✅ Yes | Active |
| mary_student | password123 | Student | STU/12346 | ✅ Yes | Active |
| dr_omondi | password123 | Staff | STF/67890 | ✅ Yes | Active |
| peter_pending | password123 | Student | STU/12347 | ❌ No | Pending |
| jane_staff | password123 | Staff | STF/67891 | ✅ Yes | Active |

### 3. **Bicycles (10)**

| Name | Model | Rate/hr | Status | Station | Serial |
|------|-------|---------|--------|---------|--------|
| Mountain Cruiser Pro | Trek X-Caliber 8 | KES 50 | Available | LIB | TRK2024001 |
| City Comfort Bike | Giant Escape 3 | KES 40 | Available | LIB | GNT2024002 |
| Speed Racer | Specialized Allez | KES 60 | Available | ENG | SPC2024003 |
| Campus Cruiser | Schwinn Discover | KES 35 | Available | ENG | SCH2024004 |
| Trail Blazer | Cannondale Trail 5 | KES 55 | Available | SC | CND2024005 |
| Urban Explorer | Trek FX 2 | KES 45 | Available | SC | TRK2024006 |
| Easy Rider | Giant Sedona DX | KES 40 | Available | HOST | GNT2024007 |
| Quick Commuter | Raleigh Cadent 2 | KES 50 | Maintenance | HOST | RAL2024008 |
| Campus Classic | Schwinn Wayfarer | KES 45 | Available | LIB | SCH2024009 |
| Sport Tourer | Trek Domane AL 2 | KES 55 | Available | ENG | TRK2024010 |

### 4. **Sample Rentals (3 completed)**
- John's past rentals with Mountain Cruiser Pro and Speed Racer
- Mary's past rental with City Comfort Bike

### 5. **Maintenance Log (1)**
- Quick Commuter under maintenance for brake and gear service

---

## 🧪 Testing Scenarios

### Scenario 1: Student Registration & Login
```bash
1. Register new student account
2. Wait for admin verification
3. Login as admin, verify the user
4. Login as student
```

### Scenario 2: Browse & Reserve Bicycle
```bash
1. Login as: john_student / password123
2. Browse available bicycles
3. Reserve "Mountain Cruiser Pro"
4. Start rental within 30 minutes
5. View active rental
```

### Scenario 3: Complete Rental Flow
```bash
1. Login as: mary_student / password123
2. Reserve "City Comfort Bike"
3. Start rental
4. Wait a few minutes
5. Return bicycle at different station
6. View rental history and receipt
```

### Scenario 4: Admin Management
```bash
1. Login to /admin with superuser
2. Verify pending user (peter_pending)
3. Add new bicycle
4. Change bicycle status
5. View all rentals
6. Add penalty to user
```

### Scenario 5: Late Return
```bash
1. Create rental in admin panel
2. Set start_time to 25+ hours ago
3. View rental as user
4. Check late fee calculation
5. Return bicycle
```

### Scenario 6: Staff Account
```bash
1. Login as: dr_omondi / password123
2. Browse bicycles
3. Make reservation as staff member
4. Complete rental
```

### Scenario 7: Unverified User
```bash
1. Login as: peter_pending / password123
2. Try to reserve bicycle
3. See verification required message
```

---

## 🔄 Reset Test Data

To completely reset and reload test data:

```bash
# Delete database
rm db.sqlite3

# Run migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

# Load test data
python3 create_test_data.py
```

---

## 📝 Manual Testing Checklist

### User Registration
- [ ] Register with student ID
- [ ] Register with staff ID
- [ ] Upload university ID document
- [ ] Receive pending verification status

### Bicycle Management
- [ ] View bicycle list
- [ ] Filter by station
- [ ] Filter by price range
- [ ] Search by name/model
- [ ] View bicycle details
- [ ] See real-time availability

### Reservation System
- [ ] Make reservation
- [ ] See 30-minute countdown
- [ ] Cancel reservation
- [ ] Reservation auto-expires after 30 min
- [ ] Cannot make multiple reservations

### Rental Flow
- [ ] Start rental from reservation
- [ ] View active rental
- [ ] See real-time cost update
- [ ] Return bicycle
- [ ] Choose return station
- [ ] Add return notes
- [ ] View receipt

### Cost Calculation
- [ ] Base cost = hourly_rate × hours
- [ ] Late fee after 24 hours
- [ ] Damage fee added if applicable
- [ ] Total cost displayed correctly

### Admin Features
- [ ] Verify users
- [ ] Add/edit bicycles
- [ ] Change bicycle status
- [ ] View all rentals
- [ ] Override rental status
- [ ] Add/resolve penalties
- [ ] View maintenance logs

### Email Notifications
- [ ] Reservation confirmation
- [ ] Rental start notification
- [ ] Rental end notification
- [ ] Overdue reminder (check console)

---

## 🐛 Troubleshooting

### Users can't login
**Check:** Is the user verified?
```python
python3 manage.py shell
>>> from apps.accounts.models import User
>>> user = User.objects.get(username='john_student')
>>> user.is_verified = True
>>> user.save()
```

### No bicycles showing
**Check:** Are bicycles marked as available?
```python
>>> from apps.bicycles.models import Bicycle
>>> Bicycle.objects.filter(status='available').count()
>>> # Update status if needed
>>> Bicycle.objects.all().update(status='available')
```

### Reservation won't start rental
**Check:** Is reservation still active?
```python
>>> from apps.rentals.models import Reservation
>>> res = Reservation.objects.filter(user=user, status='active').first()
>>> res.is_active  # Should be True
>>> res.expires_at  # Should be in future
```

---

## 📊 Data Verification

Check all data was created:

```bash
python3 manage.py shell
```

```python
from apps.accounts.models import User
from apps.stations.models import Station
from apps.bicycles.models import Bicycle
from apps.rentals.models import Rental

print(f"Users: {User.objects.count()}")
print(f"Stations: {Station.objects.count()}")
print(f"Bicycles: {Bicycle.objects.count()}")
print(f"Rentals: {Rental.objects.count()}")

# Check verified users
verified = User.objects.filter(is_verified=True).count()
print(f"Verified users: {verified}")

# Check available bikes
available = Bicycle.objects.filter(status='available').count()
print(f"Available bikes: {available}")
```

---

## 🎓 Next Steps After Testing

1. **Customize Data**
   - Edit `create_test_data.py` to add more users/bikes
   - Adjust prices and capacities
   - Add more stations

2. **Production Data**
   - Use admin panel to add real bicycles
   - Import actual student/staff data
   - Set up real email server

3. **Advanced Testing**
   - Test concurrent reservations
   - Test payment integration
   - Load test with many users
   - Test mobile responsiveness

---

## 📞 Support

If test data isn't loading correctly:
1. Check logs: `logs/django.log`
2. Run: `python3 manage.py check`
3. Verify migrations: `python3 manage.py showmigrations`
4. Reset database and try again