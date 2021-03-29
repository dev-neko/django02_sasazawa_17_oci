web: gunicorn config.wsgi
worker: celery -A config worker -l INFO --pool=solo --loglevel=INFO