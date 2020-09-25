from django.urls import path
from . import views
app_name='projectmanager'
urlpatterns = [
    path('',views.BasicView().home,name='home'),
    path('search/',views.BasicView().search,name='search'),
    path('project_category/<int:category_id>/',views.BasicView().home,name='project_category'),
    path('project/<int:project_id>/',views.ProjectView().project,name='project'),
    path('work_unit/<int:work_unit_id>/',views.ProjectView().work_unit,name='work_unit'),
    path('material/<int:material_id>/',views.MaterialView().material,name='material'),
    path('priority/',views.BasicView().priority,name='priority'),
    path('chart/',views.BasicView().chart,name='chart'),
]
