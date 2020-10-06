from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required

app_name='projectmanager'
urlpatterns = [
    path('',login_required(views.BasicView().home),name='home'),
    path('resume/',views.BasicView().resume,name='resume'),
    path('add_issue/',views.ManagerPageView().add_issue,name='add_issue'),
    # path('add_link/',login_required(views.ManagerPageView().add_link),name='add_link'),
    path('tag/<int:tag_id>/',views.ManagerPageView().tag,name='tag'),
    
    path('add_link/', permission_required(app_name+'.add_link')(views.ManagerPageView().add_link),name='add_link'),
    
    path('add_document/',views.ManagerPageView().add_document,name='add_document'),
    path('add_tag/',views.ManagerPageView().add_tag,name='add_tag'),
    path('search/',views.BasicView().search,name='search'),

    path('projectcategory/<int:category_id>/',views.BasicView().home,name='project_category'),
    path('issue/<int:issue_id>/',views.ManagerPageView().issue,name='issue'),
    path('assignment/<int:assignment_id>/',views.ManagerPageView().assignment,name='assignment'),
    path('page/<int:page_id>/',views.ManagerPageView().page,name='page'),
    path('assignment/<int:assignment_id>/',views.ManagerPageView().assignment,name='assignment'),
    path('project/<int:project_id>/',views.ManagerPageView().project,name='project'),
    path('project_avo/<int:project_id>/',views.ManagerPageView().project_avo,name='project_avo'),
    path('workunit/<int:work_unit_id>/',views.ManagerPageView().work_unit,name='work_unit'),
    path('material_category/<int:category_id>/',views.ManagerPageView().category,name='material_category'),
    path('materialrequest/<int:material_request_id>/',views.ManagerPageView().material_request,name='material_request'),
    path('materialwarehouse/<int:materialwarehouse_id>/',views.ManagerPageView().materialwarehouse,name='materialwarehouse'),
    path('materialobject/<int:materialobject_id>/',views.ManagerPageView().materialobject,name='materialobject'),
    path('materialbrand/<int:materialbrand_id>/',views.ManagerPageView().materialbrand,name='materialbrand'),
    path('material/<int:material_id>/',views.ManagerPageView().material,name='material'),
    path('priority/',views.BasicView().priority,name='priority'),
    path('add_material_request/',views.ManagerPageView().add_material_request,name='add_material_request'),
    path('sign_material_request/',views.ManagerPageView().sign,name='sign_material_request'),
    path('chart/',views.BasicView().chart,name='chart'), 
]
