#!/bin/bash

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Start seeding in the background if needed
# The seed_users command already checks if users exist
echo "Starting seeding process in the background..."
python manage.py seed_users 500000 --batch-size 25000 &

# Start Gunicorn
echo "Starting Gunicorn..."
gunicorn users_project.wsgi --bind 0.0.0.0:$PORT
