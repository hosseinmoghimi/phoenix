
from pathlib import Path
import os
import dj_database_url
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY="cz5^v3qa%kxwwlidp&&l)vy3@z78j#^u7mm+c4b)+@yjs42k6x"

DEBUG =False

ALLOWED_HOSTS = ['protected-basin-66877.herokuapp.com']

MYSQL=False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_local_1.sqlite3'),
    }
}

TIME_ZONE = 'Asia/Tehran'

SITE_URL='/'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = '/tmp/build_a0a16dbb/staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


ADMIN_URL=SITE_URL+'admin/'
# STATIC_URL = SITE_URL+'static/'

# STATIC_ROOT = '/app/staticfiles/'

MEDIA_URL =  SITE_URL+'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# STATICFILES_DIRS=['/app/static/']
PUSHER_IS_ENABLE=False
REMOTE_MEDIA=False
COMING_SOON=False
DOWNLOAD_ROOT=os.path.join(BASE_DIR, 'download')