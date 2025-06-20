#!/usr/bin/env sh

# Load variables from .env
# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs)

echo "Waiting for PostgreSQL at $DATABASE_HOST:$DATABASE_PORT..."

# Wait until the database becomes available
until timeout 1 bash -c "</dev/tcp/$DATABASE_HOST/$DATABASE_PORT" 2>/dev/null; do
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







##!/usr/bin/env bash
#
## [bash_init]-[BEGIN]
## Exit whenever it encounters an error, also known as a non–zero exit code.
#set -o errexit
## Return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status,
##   or zero if all commands in the pipeline exit successfully.
#set -o pipefail
## Treat unset variables and parameters other than the special parameters ‘@’ or ‘*’ as an error when performing parameter expansion.
#set -o nounset
## Print a trace of commands.
#set -o xtrace
## [bash_init]-[END]
#
## Apply database migrations.
#make migrate
#
## Run application.
#python manage.py runserver 0.0.0.0:8000