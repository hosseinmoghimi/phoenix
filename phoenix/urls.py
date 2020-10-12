from django.contrib import admin
from django.urls import path,include


# from django.conf import settings
from .settings import MEDIA_URL,MEDIA_ROOT,STATIC_URL,STATIC_ROOT,DEBUG
from django.views.static import serve 
from django.conf.urls import url
from .settings import SERVER_ON_HEROKU
from app.feeder import LatestEntriesFeed,SiteMapFeeder

urlpatterns = [
    path('', include('app.urls')),
    path('phoenix_app/', include('app.urls')),
    
    path('pusher/', include('leopusher.urls')),
    path('tutorial/', include('tutorial.urls')),
    path('projectmanager/', include('projectmanager.urls')),
    path('transport/', include('transport.urls')),
    path('phoenix_api/', include('phoenix_api.urls')),
    path('accounting/', include('accounting.urls')),
    path('fa/', include('app.urls')),
    path('en/', include('engapp.urls')),
    path('automation/', include('automation.urls')),
    path('market/', include('market.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('authentication.urls')),
    path('', include('authentication.urls')),    
    path('rss/', LatestEntriesFeed(),name='feeder'),
    path('sitemap/', SiteMapFeeder(),name='sitemap'),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': MEDIA_ROOT}),
      
]#+ static(STATIC_URL, document_root=STATIC_ROOT)
if SERVER_ON_HEROKU:
    from django.conf.urls.static import static
    urlpatterns=urlpatterns+static(STATIC_URL, document_root=STATIC_ROOT)



