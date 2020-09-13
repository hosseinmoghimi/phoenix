
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


DEBUG =False


ALLOWED_HOSTS = ['www.khafonline.com','khafonline.com']

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

SITE_URL='/phoenix_v1/'


ADMIN_URL=SITE_URL+'admin/'
STATIC_URL = SITE_URL+'static/'

STATIC_ROOT = '/home/khafonli/public_html/phoenix_v1/staticfiles/'

MEDIA_URL =  SITE_URL+'media/'
MEDIA_ROOT = '/home/khafonli/public_html/phoenix_v1/media/'
STATICFILES_DIRS=['/home/khafonli/phoenix_v1/static/']
PUSHER_IS_ENABLE=False
REMOTE_MEDIA=False
COMING_SOON=False
DOWNLOAD_ROOT=os.path.join(BASE_DIR,'download')