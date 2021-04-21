release: python manage.py migrate
web: gunicorn config.wsgi
worker: python manage.py custom_command