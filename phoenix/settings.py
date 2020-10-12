
from pathlib import Path
import os
import sys
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


SERVER_ON_PARS=False
SERVER_ON_HEROKU=False
SERVER_ON_LOCAL=False
SERVER_ON_AZURE=False



SERVER_ON_PARS=True
# SERVER_ON_AZURE=True
# SERVER_ON_HEROKU=True
# SERVER_ON_LOCAL=True




SERVER_KHAFONLI=False
SERVER_MAJD=False
SERVER_HAMES=False

SERVER_KHAFONLI=True
# SERVER_MAJD=True
# SERVER_HAMES=True

if '--no-color' in sys.argv or SERVER_ON_LOCAL:
    SERVER_ON_LOCAL=True  
    SERVER_ON_HEROKU=False
    SERVER_ON_PARS=False
    SERVER_ON_AZURE=False
    from . import settings_local as server_settings
elif SERVER_ON_AZURE:
    SERVER_ON_AZURE=True  
    SERVER_ON_HEROKU=False
    SERVER_ON_PARS=False
    SERVER_ON_LOCAL=False
    from . import settings_azure as server_settings
    SECRET_KEY = server_settings.SECRET_KEY
    
elif SERVER_ON_PARS:
    SERVER_ON_LOCAL=False  
    SERVER_ON_HEROKU=False
    SERVER_ON_PARS=True
    if SERVER_HAMES:
        from . import settings_hames as server_settings
    if SERVER_MAJD:
        from . import settings_majd as server_settings
    if SERVER_KHAFONLI:
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
    'tutorial',
    'leopusher',
    'projectmanager',
    'transport',
    'accounting',
    'app',
    'phoenix_api',
    'automation',
    'engapp',
    'market',
    'authentication',
    'django_cleanup',
    'django_social_share',
    'rest_framework',
    'djecrety',
    'tinymce',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MIDDLEWARE_CLASSES = [
    'app.get_username.RequestMiddleware',
    ]

if SERVER_ON_HEROKU and False: 
    MIDDLEWARE_CLASSES = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'app.get_username.RequestMiddleware',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates'),'templates'],
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
SITE_DOMAIN = server_settings.SITE_DOMAIN
if SERVER_ON_HEROKU:    
    import django_heroku
    django_heroku.settings(locals())
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
