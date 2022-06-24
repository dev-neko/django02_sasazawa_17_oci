import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

# Trueの場合は本番環境でもエラー内容が表示される
DEBUG=False
# DEBUG=True

ALLOWED_HOSTS=['*']

# Herokuの環境変数からSECRET_KEYを取得、取得できないときは空
SECRET_KEY=os.environ.get('SECRET_KEY')

# ajaxへpostする際のサイズ上限を指定
# DATA_UPLOAD_MAX_MEMORY_SIZE = None

INSTALLED_APPS = [
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'applications.apps.ApplicationsConfig',
]

MIDDLEWARE = [
		'django.middleware.security.SecurityMiddleware',
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
		'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
		{
				'BACKEND': 'django.template.backends.django.DjangoTemplates',
				'DIRS': [os.path.join(BASE_DIR, 'templates')],
				'APP_DIRS': True,
				'OPTIONS': {
						'context_processors': [
								'django.template.context_processors.debug',
								'django.template.context_processors.request',
								'django.contrib.auth.context_processors.auth',
								'django.contrib.messages.context_processors.messages',
						],
				},
		},
]

WSGI_APPLICATION = 'config.wsgi.application'

import dj_database_url
DATABASES = {
		'default': dj_database_url.config(),
}

AUTH_PASSWORD_VALIDATORS = [
		{
				'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
		},
		{
				'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
		},
		{
				'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
		},
		{
				'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
		},
]

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# https://devcenter.heroku.com/ja/articles/django-assets
# Heroku推奨の方法
STATIC_URL = '/static/'
STATICFILES_DIRS = (
		os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# この処理を追加することで settings.py の DEBUG が False でも local_settings があればデバッグ環境だと判断されて runserver が可能になる→DEBUGを切り替える必要もなくなる
try:
		from .local_settings import *
except ImportError:
		pass

# Authentication
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'