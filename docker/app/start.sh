#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -o errexit
# The return value of a pipeline is the value of the last command to exit with a non-zero status.
set -o pipefail
# Treat unset variables as an error and exit immediately.
set -o nounset
# Print commands and their arguments as they are executed.
set -o xtrace

# Apply database migrations
make migrate

# Create a superuser if it does not exist
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

# Start Django server
python manage.py runserver 0.0.0.0:8000