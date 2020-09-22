from django.urls import path
from . import apis
app_name='phoenix_api'
urlpatterns = [
    
    path('login/',apis.AuthApi().login,name='login'),


    path('check_available_username/',apis.AuthApi().check_available_username,name='check_available_username'),
    path('add_notification/',apis.NotificationApi().add_notification,name='add_notification'),


]
