import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent.parent
SECRET_KEY=os.getenv('DJANGO_SECRET_KEY')
DEBUG=os.getenv('DJANGO_DEBUG')=='True'
ALLOWED_HOSTS=os.getenv('ALLOWED_HOSTS').split(',')
INSTALLED_APPS=[
 'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
 'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
 'rest_framework','rest_framework_simplejwt','users_app'
]
MIDDLEWARE=[ 'django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware',]
ROOT_URLCONF='users_project.urls'
WSGI_APPLICATION='users_project.wsgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':os.getenv('POSTGRES_DB'),
 'USER':os.getenv('POSTGRES_USER'),'PASSWORD':os.getenv('DB_PASSWORD'),
 'HOST':os.getenv('DB_HOST'),'PORT':os.getenv('DB_PORT'),}}
REST_FRAMEWORK={
 'DEFAULT_AUTHENTICATION_CLASSES':('rest_framework_simplejwt.authentication.JWTAuthentication',),
 'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.IsAuthenticated',),
}
