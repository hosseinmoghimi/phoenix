
from django.urls import path
from . import views
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicView().home,name='home'),
]
