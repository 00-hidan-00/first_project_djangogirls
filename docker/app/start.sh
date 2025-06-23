#!/usr/bin/env sh

# Load variables from .env
# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs)

echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."

# Wait until the database becomes available
until timeout 1 bash -c "</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT" 2>/dev/null; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - running migrations"

# Apply migrations
make migrate

echo "Starting Django server"

# Create a superuser if it does not exist
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')"

# Start the server
python manage.py runserver 0.0.0.0:8000