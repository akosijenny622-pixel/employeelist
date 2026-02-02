#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install --upgrade -r requirements.txt

# Navigate to the config directory where manage.py is located
cd config

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Create admin user if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating admin user..."
    python manage.py create_admin
fi
