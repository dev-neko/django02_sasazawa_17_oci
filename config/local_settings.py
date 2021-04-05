import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES={
    'default':{
        'ENGINE':'django.db.backends.sqlite3',
        'NAME':os.path.join(BASE_DIR,'db.sqlite3'),
    }
}

DEBUG=True

SECRET_KEY='0c2mr9p-mjjf7490d7i!2i!)*th*ii)dd4efvijnrx1f8xwdc*'