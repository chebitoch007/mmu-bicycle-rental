#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Load initial data (optional)
python manage.py loaddata fixtures/stations.json || echo "Fixtures already loaded"