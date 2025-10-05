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

# Create superuser if it doesn't exist
python manage.py shell -c "
import os
from django.contrib.auth.models import User
username = 'superuser'
email = 'admin@example.com'
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
"