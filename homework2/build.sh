#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Move into the Django project directory (where manage.py lives)
cd movie_theater_booking

# Run Django management commands
python manage.py collectstatic --no-input
python manage.py migrate
