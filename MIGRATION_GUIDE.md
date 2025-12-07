# Database Migration Guide

## Initial Setup

### Step 1: Backup (if needed)
```bash
python manage.py dumpdata > backup.json
```

### Step 2: Delete existing migrations (if starting fresh)
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
```

### Step 3: Delete database (development only)
```bash
rm db.sqlite3  # For SQLite
# OR for PostgreSQL: DROP DATABASE mmu_bicycle_rental;
```

### Step 4: Create fresh migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations stations
python manage.py makemigrations bicycles
python manage.py makemigrations rentals
python manage.py makemigrations payments
```

### Step 5: Run migrations
```bash
python manage.py migrate
```

### Step 6: Create superuser
```bash
python manage.py createsuperuser
```

## Common Migration Issues

### Issue 1: "No such table: accounts_user"
**Solution:** Run migrations in order:
```bash
python manage.py migrate accounts
python manage.py migrate
```

### Issue 2: Circular dependency between apps
**Solution:** Check ForeignKey imports and use string references:
```python
# Instead of:
from apps.bicycles.models import Bicycle

# Use:
bicycle = models.ForeignKey('bicycles.Bicycle', ...)
```

### Issue 3: Custom user model conflicts
**Solution:** Ensure AUTH_USER_MODEL is set before first migration:
```python
# config/settings/base.py
AUTH_USER_MODEL = 'accounts.User'
```

## Production Migration

### Before deployment:
1. Test migrations locally
2. Backup production database
3. Run migrations during low-traffic period

```bash
# Production migration commands
python manage.py migrate --check
python manage.py migrate --plan
python manage.py migrate
```

## Rollback (if needed)

```bash
# Rollback to specific migration
python manage.py migrate accounts 0001

# Show migration history
python manage.py showmigrations
```