import os
import subprocess


# cmd="pip install -r requirements.txt"
# subprocess.run(cmd.split(' '))

cmd="python manage.py collectstatic --noinput"
subprocess.run(cmd.split(' '))

# CA証明書をDLする
cmd=os.getenv("DOWNLOAD_CA_CERT")
subprocess.run(cmd.split(' '))

cmd="python manage.py makemigrations"
subprocess.run(cmd.split(' '))

cmd="python manage.py migrate"
subprocess.run(cmd.split(' '))

cmd="python manage.py runserver 0.0.0.0:3000"
subprocess.run(cmd.split(' '))