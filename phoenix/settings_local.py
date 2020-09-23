from pathlib import Path
import os
import dj_database_url
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


DEBUG = True

ALLOWED_HOSTS = ['192.168.100.198','192.168.1.21','192.168.1.7','127.0.0.1']

# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'OPTIONS': {
#                 'read_default_file': os.path.join(os.path.join(BASE_DIR, 'phoenix'),'secret_local_my_sql.cnf'),

#             },
#         }
#     }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_local_2.sqlite3'),
    }
}
# DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


MYSQL=True



TIME_ZONE = 'Asia/Tehran'

SITE_URL='/'
ADMIN_URL=SITE_URL+'admin/'
STATIC_URL = SITE_URL+'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
MEDIA_URL =  SITE_URL+'media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
PUSHER_IS_ENABLE=False
REMOTE_MEDIA=False
COMING_SOON=False
DOWNLOAD_ROOT=os.path.join(BASE_DIR,'download')