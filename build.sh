#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Navigate to the config directory where manage.py is located
cd config

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
