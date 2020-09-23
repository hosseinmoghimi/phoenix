from django.urls import path
from . import views
app_name='transport'

urlpatterns = [
    path('',views.IndexView().home,name='home'),
    
]
