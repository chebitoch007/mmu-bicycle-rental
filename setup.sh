#!/bin/bash

# MMU Bicycle Rental System - Quick Setup Script

echo "🚲 Setting up MMU Bicycle Rental System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your configuration"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p media/bicycles media/profile_pictures media/university_ids
mkdir -p staticfiles
mkdir -p logs

# Run migrations
echo "🗄️  Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Load fixtures
echo "📊 Loading sample data..."
if [ -f fixtures/stations.json ]; then
    python manage.py loaddata fixtures/stations.json
    echo "✅ Stations loaded"
fi

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Run the server: python manage.py runserver"
echo ""
echo "🚀 Visit http://localhost:8000 to see your application!"