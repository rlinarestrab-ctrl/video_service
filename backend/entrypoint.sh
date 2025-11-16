#!/bin/sh
set -e

# Solo esperar a Postgres si existe POSTGRES_HOST (local con docker-compose)
if [ -n "$POSTGRES_HOST" ]; then
  echo "⏳ Esperando a PostgreSQL en $POSTGRES_HOST:${POSTGRES_PORT:-5432} ..."
  until nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}"; do
    sleep 1
  done
  echo "✅ Base de datos disponible"
fi

echo "📦 Aplicando migraciones..."
python manage.py migrate --noinput

# Render define $PORT; en local usamos 8000 por defecto
APP_PORT=${PORT:-8000}

echo "🚀 Iniciando Gunicorn en 0.0.0.0:${APP_PORT}"
gunicorn video_service.wsgi:application --bind 0.0.0.0:${APP_PORT}
