from django.contrib import admin
from django.urls import path,include


# from django.conf import settings
from .settings import MEDIA_URL,MEDIA_ROOT,STATIC_URL,STATIC_ROOT
from django.views.static import serve 
from django.conf.urls import url
from .settings import SERVER_ON_HEROKU

urlpatterns = [
    path('fa/', include('app.urls')),
    path('en/', include('engapp.urls')),
    path('automation/', include('automation.urls')),
    path('market/', include('market.urls')),
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('app.urls')),

    url(r'^media/(?P<path>.*)$', serve,{'document_root': MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': STATIC_ROOT}),  
]#+ static(STATIC_URL, document_root=STATIC_ROOT)
if SERVER_ON_HEROKU:
    from django.conf.urls.static import static
    urlpatterns=urlpatterns+static(STATIC_URL, document_root=STATIC_ROOT)
    # urlpatterns=urlpatterns+static(MEDIA_URL, document_root=MEDIA_ROOT)


