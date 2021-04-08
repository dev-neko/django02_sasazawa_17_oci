web: gunicorn config.wsgi
worker: python manage.py custom_command
worker: celery -A config worker -l INFO