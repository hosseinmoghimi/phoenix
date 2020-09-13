
from pathlib import Path
import os
import dj_database_url
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


DEBUG =False


ALLOWED_HOSTS = ['www.hamescctv.com','hamescctv.com','www.imenyar.com','imenyar.com','www.tonusdoor.com','tonusdoor.com']

MYSQL=True


DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.path.join(os.path.join(BASE_DIR, 'phoenix'),'secret_hames_my_sql.cnf'),

            },
        }
    }


TIME_ZONE = 'Asia/Tehran'

SITE_URL='/hames/'


ADMIN_URL=SITE_URL+'admin/'
STATIC_URL = SITE_URL+'static/'

STATIC_ROOT = '/home2/imenyarc/public_html/hames/staticfiles/'

MEDIA_URL =  SITE_URL+'media/'
MEDIA_ROOT = '/home2/imenyarc/public_html/hames/media/'
STATICFILES_DIRS=['/home2/imenyarc/hames/static/']
PUSHER_IS_ENABLE=False
REMOTE_MEDIA=False
COMING_SOON=False
DOWNLOAD_ROOT=os.path.join(BASE_DIR,'download')