from django.urls import path,include
from . import views
app_name="automation"
urlpatterns = [
    path('',views.BasicView().home,name='home'), 
    path('add_work_unit/',views.WorkUnitView().add_work_unit,name='add_work_unit'),
    path('add_project/',views.WorkUnitView().add_work_unit,name='project'),
    path('add_employee/',views.WorkUnitView().add_work_unit,name='add_employee'),
    path('work_unit/<int:work_unit_id>/',views.WorkUnitView().work_unit,name='work_unit'),
    path('project/<int:project_id>/',views.ProjectView().project,name='project'),
    path('product_requests/',views.ProductRequestView().list,name='product_requests'), 
    path('product_request/<int:product_request_id>/',views.ProductRequestView().product_request,name='product_request'),    
]