#!/bin/bash
set -e

echo "=== Aplicando migraciones ==="
python manage.py makemigrations --noinput
python manage.py migrate --noinput


echo "=== Iniciando Gunicorn ==="
exec gunicorn pedregal_map.wsgi:application --timeout 120 --workers 4 --threads 2