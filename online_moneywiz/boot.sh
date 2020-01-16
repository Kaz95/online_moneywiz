#!/bin/sh
source venv/bin/activate
exec gunicorn --workers=2 -b :8000 --access-logfile - --error-logfile - wsgi:app