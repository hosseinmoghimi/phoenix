from django.urls import path
from . import views
app_name='authentication'
urlpatterns = [
    
    path('login/',views.AuthView().login,name='login'),
    path('reset_password/',views.AuthView().reset_password,name='reset_password'),
    path('auth/',views.AuthView().auth,name='auth'),
    path('register/',views.AuthView().register,name='register'),
    path('logout/',views.AuthView().logout,name='logout'),
    path('check_available_username/',views.AuthView().check_available_username,name='check_available_username'),
    
]
