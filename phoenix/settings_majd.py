
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


DEBUG =False


ALLOWED_HOSTS = ['www.nsk-majd.com','nsk-majd.com']

MYSQL=False


# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'OPTIONS': {
#                 'read_default_file': os.path.join(os.path.join(BASE_DIR, 'phoenix'),'secret_khafonli_my_sql.cnf'),

#             },
#         }
#     }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_local.sqlite3'),
    }
}

TIME_ZONE = 'Asia/Tehran'

SITE_URL='/'


ADMIN_URL=SITE_URL+'admin/'
STATIC_URL = SITE_URL+'static/'

STATIC_ROOT = '/home2/nskmajdc/public_html/phoenix/staticfiles/'

MEDIA_URL =  SITE_URL+'media/'
MEDIA_ROOT = '/home2/nskmajdc/public_html/phoenix/media/'
STATICFILES_DIRS=['/home2/nskmajdc/phoenix/static/']
PUSHER_IS_ENABLE=False
REMOTE_MEDIA=False
COMING_SOON=False
DOWNLOAD_ROOT=os.path.join(BASE_DIR,'download')