web: gunicorn config.wsgi
worker: celery -A config worker -l INFO
worker: python manage.py custom_command