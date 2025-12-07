# MMU Bicycle Rental System - Setup Checklist

## ✅ Pre-Flight Checklist

### 1. Files Verification
Run this command to check all files are present:

```bash
ls apps/accounts/{models.py,views.py,forms.py,urls.py,admin.py}
ls apps/bicycles/{models.py,views.py,forms.py,urls.py,admin.py}
ls apps/rentals/{models.py,views.py,forms.py,urls.py,admin.py}
ls apps/stations/{models.py,views.py,urls.py,admin.py}
ls apps/payments/{models.py,admin.py}
ls apps/api/urls.py
ls core/{email.py,validators.py,mixins.py,utils.py}
ls config/{urls.py,wsgi.py,asgi.py}
ls config/settings/{base.py,development.py,production.py}
```

### 2. Environment Setup

```bash
# Create .env file
cat > .env << 'EOF'
SECRET_KEY=your-secret-key-here-$(openssl rand -base64 32)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,8d68393dad6a.ngrok-free.app

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@mmu.ac.ke

SITE_URL=http://localhost:8000
EOF
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Make migrations for each app in order
python manage.py makemigrations accounts
python manage.py makemigrations stations
python manage.py makemigrations bicycles
python manage.py makemigrations rentals
python manage.py makemigrations payments

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 5. Load Sample Data

```bash
python manage.py loaddata fixtures/stations.json
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Run Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

---

## 🎯 Testing Checklist

### Account Testing
- [ ] Register new user (student)
- [ ] Login with created account
- [ ] Verify account through admin
- [ ] Update profile
- [ ] Test password reset

### Bicycle Testing
- [ ] View bicycle list
- [ ] Filter bicycles by station
- [ ] View bicycle details
- [ ] Admin: Add new bicycle
- [ ] Admin: Edit bicycle
- [ ] Admin: Change bicycle status

### Rental Flow Testing
- [ ] Reserve a bicycle
- [ ] Check reservation countdown
- [ ] Start rental from reservation
- [ ] View active rental
- [ ] Return bicycle
- [ ] View rental history
- [ ] Check cost calculation

### Admin Testing
- [ ] Login to /admin
- [ ] Verify pending users
- [ ] Manage bicycles
- [ ] View all rentals
- [ ] Override rental status
- [ ] Add penalty to user

---

## 🐛 Common Issues & Solutions

### Issue 1: "No module named 'apps.dashboard'"
**Solution:** Update config/urls.py to remove dashboard line
```python
# Remove this line:
path('dashboard/', include(('apps.dashboard.urls', 'dashboard'), namespace='dashboard')),
```

### Issue 2: "AUTH_USER_MODEL refers to model 'accounts.User' that has not been installed"
**Solution:** Run migrations in correct order:
```bash
python manage.py makemigrations accounts
python manage.py migrate accounts
python manage.py migrate
```

### Issue 3: "Table doesn't exist" errors
**Solution:** Delete database and start fresh:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue 4: Static files not loading
**Solution:** Run collectstatic and check DEBUG=True:
```bash
python manage.py collectstatic --noinput
```

### Issue 5: CSRF verification failed
**Solution:** Ensure {% csrf_token %} in all forms and check ALLOWED_HOSTS

---

## 📊 Admin Panel Setup

### After first login to /admin:

1. **Create Stations:**
   - Go to Stations → Add Station
   - Create at least 3 stations
   - Or load fixtures: `python manage.py loaddata fixtures/stations.json`

2. **Add Bicycles:**
   - Go to Bicycles → Add Bicycle
   - Set status to "Available"
   - Assign to a station

3. **Verify Users:**
   - Go to Users
   - Find pending users
   - Check "is_verified"
   - Save

4. **Monitor Rentals:**
   - Go to Rentals
   - View active rentals
   - Override if needed

---

## 🚀 Going to Production

### Before deploying:

1. **Security Settings:**
```python
# .env
DEBUG=False
SECRET_KEY=<generate-new-secure-key>
ALLOWED_HOSTS=your-domain.com
```

2. **Database:**
```python
# Use PostgreSQL
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

3. **Static Files:**
```bash
python manage.py collectstatic --noinput
```

4. **Email:**
Configure real SMTP settings in .env

5. **HTTPS:**
Enable SSL/TLS in production settings

---

## 📞 Support

If you encounter issues:

1. Check logs: `logs/django.log`
2. Run: `python manage.py check`
3. Verify all dependencies: `pip freeze`
4. Check Python version: `python --version` (need 3.10+)

---

## ✅ Success Indicators

Your system is working correctly if:

- ✅ Homepage loads without errors
- ✅ Can register and login users
- ✅ Can view bicycle list
- ✅ Can make reservations
- ✅ Countdown timer works
- ✅ Can start and complete rentals
- ✅ Email notifications appear in console
- ✅ Admin panel is accessible
- ✅ Cost calculations are correct

---

## 🎓 Next Steps

1. Customize templates with MMU branding
2. Add real bicycle data
3. Configure email server
4. Set up payment integration
5. Deploy to production server
6. Add monitoring and logging
7. Create user documentation
8. Train staff on admin panel