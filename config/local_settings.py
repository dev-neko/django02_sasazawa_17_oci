import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES={
    'default':{
        'ENGINE':'django.db.backends.sqlite3',
        'NAME':os.path.join(BASE_DIR,'db.sqlite3'),
    }
}

DEBUG=True

SECRET_KEY='gttr!^bggvptm+8h=@i4=2tc+u31fy8ab2#9=#ms^*9bomx2(z'