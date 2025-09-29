#!/usr/bin/env bash
set -euo pipefail

# Default: run migrations/collectstatic only when requested by env flags
: "${AUTO_MIGRATE:=true}"
: "${AUTO_COLLECTSTATIC:=true}"
: "${PORT:=8000}"
: "${WORKERS:=3}"
: "${THREADS:=2}"
: "${TIMEOUT:=60}"

cd /app

if [ "${AUTO_MIGRATE}" = "true" ]; then
  python manage.py migrate --noinput
fi

if [ "${AUTO_COLLECTSTATIC}" = "true" ]; then
  python manage.py collectstatic --noinput
fi

# Start Gunicorn
exec gunicorn field_mgmt.wsgi:application \
  --bind 0.0.0.0:"${PORT}" \
  --workers "${WORKERS}" \
  --threads "${THREADS}" \
  --timeout "${TIMEOUT}" \
  --log-level info
