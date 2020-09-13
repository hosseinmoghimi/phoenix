
from pathlib import Path
import os
import sys
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


SERVER_ON_PARS=True
SERVER_ON_HEROKU=False
SERVER_ON_LOCAL=False





if '--no-color' in sys.argv or SERVER_ON_LOCAL:
    SERVER_ON_LOCAL=True  
    SERVER_ON_HEROKU=False
    SERVER_ON_PARS=False
    from . import settings_local as server_settings
elif SERVER_ON_PARS:
    SERVER_ON_LOCAL=False  
    SERVER_ON_HEROKU=False
    SERVER_ON_PARS=True
    from . import settings_khafonli as server_settings


elif SERVER_ON_HEROKU:
    SERVER_ON_PARS=False
    SERVER_ON_LOCAL=False  
    SERVER_ON_HEROKU=True
    from . import settings_heroku as server_settings   
    SECRET_KEY = server_settings.SECRET_KEY
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    

# READ SECRET_KEY FROM SECURE UNTRACKED FILE
if not SERVER_ON_HEROKU:
    try:        
        from .secret_key import SECRET_KEY_FROM_FILE
        SECRET_KEY=SECRET_KEY_FROM_FILE
    except :
        if SERVER_ON_LOCAL:
            secret_file_content="""SECRET_KEY_FROM_FILE = 'yj)%c-)__z_null-_l-ned!$6*cs)_=w@g&t=0vj^wg)knwm3z'"""
            f = open('phoenix/secret_key.py', 'w')  # open file in write mode
            f.write(secret_file_content)
            f.close()
            from .secret_key import SECRET_KEY_FROM_FILE
            SECRET_KEY=SECRET_KEY_FROM_FILE






# Application definition

INSTALLED_APPS = [
    'app',
    'market',
    'authentication',    
    'django_cleanup',
    'rest_framework',
    'djecrety',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


if SERVER_ON_HEROKU and False: 
    MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware'
    ]
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]


ROOT_URLCONF = 'phoenix.urls'

TEMPLATES = [
    
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'app.views.getContext',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'phoenix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'



USE_I18N = True

USE_L10N = True

USE_TZ = True

ADMIN_URL=server_settings.ADMIN_URL
ALLOWED_HOSTS = server_settings.ALLOWED_HOSTS
COMING_SOON=server_settings.COMING_SOON
DATABASES=server_settings.DATABASES
DEBUG = server_settings.DEBUG
DOWNLOAD_ROOT=server_settings.DOWNLOAD_ROOT
MEDIA_ROOT = server_settings.MEDIA_ROOT
MEDIA_URL = server_settings.MEDIA_URL
MYSQL=server_settings.MYSQL
PUSHER_IS_ENABLE=server_settings.PUSHER_IS_ENABLE
REMOTE_MEDIA=server_settings.REMOTE_MEDIA
# SECRET_KEY = server_settings.SECRET_KEY
SITE_URL=server_settings.SITE_URL
STATIC_ROOT = server_settings.STATIC_ROOT
STATIC_URL = server_settings.STATIC_URL
STATICFILES_DIRS=server_settings.STATICFILES_DIRS
TIME_ZONE = server_settings.TIME_ZONE
if SERVER_ON_HEROKU:    
    import django_heroku
    django_heroku.settings(locals())
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
