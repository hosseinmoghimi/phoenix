from django.urls import path
from . import views
app_name='projectmanager'
urlpatterns = [
    path('',views.BasicView().home,name='home'),
    path('search/',views.BasicView().search,name='search'),
    path('project_category/<int:category_id>/',views.BasicView().home,name='project_category'),
    path('project/<int:project_id>/',views.BasicView().home,name='project'),
]
