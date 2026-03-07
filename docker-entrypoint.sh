#!/bin/bash
set -e

python manage.py migrate --noinput

python manage.py collectstatic --noinput --clear


exec uvicorn mysite.asgi:application --host 0.0.0.0 --port 8000 --workers 3