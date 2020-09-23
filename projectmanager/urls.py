from django.urls import path
from . import views
app_name='projectmanager'
urlpatterns = [
    path('',views.BasicView().home,name='home'),
]
