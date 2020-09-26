from django.urls import path
from . import views
app_name='projectmanager'
urlpatterns = [
    path('',views.BasicView().home,name='home'),
    path('search/',views.BasicView().search,name='search'),
    path('projectcategory/<int:category_id>/',views.BasicView().home,name='project_category'),
    path('issue/<int:page_id>/',views.BasicView().page,name='issue'),
    path('page/<int:page_id>/',views.BasicView().page,name='page'),
    path('project/<int:project_id>/',views.ProjectView().project,name='project'),
    path('workunit/<int:work_unit_id>/',views.ProjectView().work_unit,name='work_unit'),
    path('material_category/<int:category_id>/',views.MaterialView().category,name='material_category'),
    path('materialrequest/<int:material_request_id>/',views.MaterialRequestView().material_request,name='material_request'),
    path('material/<int:material_id>/',views.MaterialView().material,name='material'),
    path('priority/',views.BasicView().priority,name='priority'),
    path('add_material_request/',views.MaterialRequestView().add_material_request,name='add_material_request'),
    path('sign_material_request/',views.MaterialRequestView().sign,name='sign_material_request'),
    path('chart/',views.BasicView().chart,name='chart'), 
]
