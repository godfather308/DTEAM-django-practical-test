#!/bin/sh

set -e

echo "Running database migrations..."
python src/manage.py migrate

echo "Starting Django server..."
python src/manage.py runserver 0.0.0.0:8000
