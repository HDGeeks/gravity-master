#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $DB_HOST -U $POSTGRES_USER -c '\q'; do
  >&2 echo "PostgreSQL is not ready yet - waiting"
  sleep 1
done

>&2 echo "PostgreSQL is ready"

# Check and apply migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django application
exec gunicorn your_project_name.wsgi:application --bind 0.0.0.0:8000 --workers 3