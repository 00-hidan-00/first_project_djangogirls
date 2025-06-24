#!/usr/bin/env bash

# [bash_init]-[BEGIN]
# Exit immediately if a command exits with a non-zero status.
set -o errexit
# The return value of a pipeline is the value of the last command to exit with a non-zero status.
set -o pipefail
# Treat unset variables as an error and exit immediately.
set -o nounset
# [bash_init]-[END]

# [wait_postgres]-[BEGIN]
# Function to check PostgreSQL readiness using psycopg
postgres_ready() {
  python - <<END
import sys
import psycopg

try:
    conn = psycopg.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
    conn.close()
except psycopg.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."

until postgres_ready; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up"
# [wait_postgres]-[END]

# Execute the command passed as arguments (usually CMD)
exec "$@"