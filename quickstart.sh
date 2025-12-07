#!/bin/bash

# MMU Bicycle Rental System - Quick Start Script
# This script sets up everything automatically

set -e  # Exit on error

echo "🚲 MMU Bicycle Rental System - Quick Start"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version found"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
SECRET_KEY=django-insecure-change-this-in-production-$(openssl rand -base64 32)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,8d68393dad6a.ngrok-free.app

DATABASE_URL=sqlite:///db.sqlite3

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=MMU Bicycle Rental <noreply@mmu.ac.ke>

SITE_URL=http://localhost:8000
SITE_NAME=MMU Bicycle Rental
EOF
    echo "✅ Created .env file"
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p media/{bicycles,profile_pictures,university_ids}
mkdir -p staticfiles
echo "✅ Directories created"

# Create API urls if missing
if [ ! -f apps/api/urls.py ]; then
    echo "📝 Creating apps/api/urls.py..."
    cat > apps/api/urls.py << 'EOF'
from django.urls import path

app_name = 'api'

urlpatterns = [
    # API endpoints will be added here
]
EOF
    echo "✅ Created apps/api/urls.py"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Clean up old migrations (optional)
read -p "🗑️  Remove old migrations and start fresh? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing old migrations..."
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" -delete
    rm -f db.sqlite3
    echo "✅ Old data removed"
fi

# Create migrations
echo "🗄️  Creating migrations..."
python3 manage.py makemigrations accounts || { echo "❌ Failed to create accounts migrations"; exit 1; }
python3 manage.py makemigrations stations || { echo "❌ Failed to create stations migrations"; exit 1; }
python3 manage.py makemigrations bicycles || { echo "❌ Failed to create bicycles migrations"; exit 1; }
python3 manage.py makemigrations rentals || { echo "❌ Failed to create rentals migrations"; exit 1; }
python3 manage.py makemigrations payments || { echo "❌ Failed to create payments migrations"; exit 1; }
echo "✅ Migrations created"

# Apply migrations
echo "🗄️  Applying migrations..."
python3 manage.py migrate || { echo "❌ Failed to apply migrations"; exit 1; }
echo "✅ Migrations applied"

# Load fixtures
if [ -f fixtures/stations.json ]; then
    echo "📊 Loading sample data..."
    python3 manage.py loaddata fixtures/stations.json || echo "⚠️  Could not load stations fixture"
    echo "✅ Sample data loaded"
fi

# Collect static files
echo "📦 Collecting static files..."
python3 manage.py collectstatic --noinput --clear > /dev/null 2>&1
echo "✅ Static files collected"

# Create superuser
echo ""
echo "👤 Creating superuser account..."
echo "Please enter superuser details:"
python3 manage.py createsuperuser

# Final checks
echo ""
echo "🔍 Running system checks..."
python3 manage.py check || { echo "❌ System check failed"; exit 1; }
echo "✅ System checks passed"

# Success message
echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo "=========================================="
echo ""
echo "🚀 To start the development server, run:"
echo -e "${YELLOW}   python3 manage.py runserver${NC}"
echo ""
echo "📱 Then visit:"
echo "   - Homepage: http://localhost:8000"
echo "   - Admin Panel: http://localhost:8000/admin"
echo ""
echo "📚 Next steps:"
echo "   1. Login to admin panel"
echo "   2. Verify your user account"
echo "   3. Add bicycles and stations"
echo "   4. Test the rental flow"
echo ""
echo "📖 See SETUP_CHECKLIST.md for detailed testing guide"
echo ""