#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p media/bicycles
mkdir -p media/profile_pictures
mkdir -p media/university_ids

# Collect static files
python3 manage.py collectstatic --no-input

# Run migrations
python3 manage.py migrate

# Load initial data (optional)
python3 manage.py loaddata fixtures/stations.json || echo "Fixtures already loaded"