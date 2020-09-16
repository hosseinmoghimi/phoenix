from django.urls import path,include
from . import views
app_name="automation"
urlpatterns = [
    path('',views.BasicView().home,name='home'), 
    path('work_unit/<int:work_unit_id>/',views.WorkUnitView().work_unit,name='work_unit'),
    path('project/<int:project_id>/',views.WorkUnitView().work_unit,name='project'),
    path('product_requests/',views.ProductRequestView().list,name='product_requests'), 
    path('product_request/<int:product_request_id>/',views.ProductRequestView().product_request,name='product_request'),    
]