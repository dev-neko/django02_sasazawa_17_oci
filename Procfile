release: python manage.py migrate
web: gunicorn config.wsgi
worker: python script/v14.py