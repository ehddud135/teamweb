#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "PostgreSQL is up."

python /app/seteamweb/manage.py migrate --noinput

exec gunicorn --chdir /app/seteamweb --bind 0.0.0.0:8000 core.wsgi:application