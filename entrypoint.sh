#!/bin/sh
# wait for db to be ready (simple loop)
until python manage.py migrate --noinput; do
  echo "Waiting for DB..."
  sleep 2
done

# collect static (optional for now)
python manage.py collectstatic --noinput || true

# run migrations completed, now exec the passed command
exec "$@"