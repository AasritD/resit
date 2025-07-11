import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG')=='True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

INSTALLED_APPS = [
  'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
  'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
  'rest_framework','inference_app',
]

# Use BigAutoField by default for primary keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inference_project.urls'
WSGI_APPLICATION = 'inference_project.wsgi.application'

# TEMPLATES config required for the admin site
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],            # you can add project-wide template dirs here
        'APP_DIRS': True,      # look for templates inside each app
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


DATABASES = {
  'default': {
    'ENGINE':'django.db.backends.postgresql',
    'NAME':os.getenv('POSTGRES_DB'),
    'USER':os.getenv('POSTGRES_USER'),
    'PASSWORD':os.getenv('DB_PASSWORD'),
    'HOST':os.getenv('DB_HOST'),
    'PORT':os.getenv('DB_PORT'),
  }
}

STATIC_URL = '/static/'

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES':(
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
  ),
  'DEFAULT_PERMISSION_CLASSES':(
    'rest_framework.permissions.IsAuthenticated',
  ),
}
