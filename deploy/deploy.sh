#!/usr/bin/env bash
set -e

cd /home/deploy/app

if [ ! -f .env.production ]; then
  echo ".env.production missing - abort!"
  exit 1
fi

docker compose pull
docker compose up -d --remove-orphans --force-recreate

if [ "${AUTO_MIGRATE:-true}" = "true" ]; then
  echo "Running migrations..."
  docker compose exec -T web python manage.py migrate --noinput
fi

docker image prune -f || true
