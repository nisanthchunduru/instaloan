#!/bin/bash

# Function to wait for the PostgreSQL database to be ready
wait_for_postgres() {
  until nc -z -v -w30 postgres 5432; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 5
  done
  echo "PostgreSQL is ready"
}

# Function to run database migrations
run_migrations() {
  flask db upgrade
}

# Check if migrations need to be run
if [ ! -f "migrations/versions" ]; then
  echo "Running initial database setup..."
  wait_for_postgres
  flask db init
  run_migrations
fi

# Start the Flask application
exec "$@"
