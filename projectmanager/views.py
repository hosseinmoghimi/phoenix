from django.shortcuts import render,redirect,reverse
from .forms import *
from django.views import View
from django.http import Http404
from app.views import getContext as AppContext
from .repo import ProjectRepo,ProjectCategoryRepo,WorkUnitRepo
from .apps import APP_NAME
TEMPLATE_ROOT='projectmanager/'
def getContext(request):
    user=request.user
    context=AppContext(request)
    context['APP_NAME']=APP_NAME
    context['search_form']=SearchForm()
    context['search_url']=reverse('projectmanager:search')
    return context
class BasicView(View):
    def home(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['project_categories']=ProjectCategoryRepo(user=user).list()
        context['projects']=ProjectRepo(user=user).list()
        context['work_units']=WorkUnitRepo(user=user).list()
        return render(request,TEMPLATE_ROOT+'index.html',context)
 
        
    def search(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['project_categories']=ProjectCategoryRepo(user=user).list()
        context['projects']=ProjectRepo(user=user).list()
        return render(request,TEMPLATE_ROOT+'search.html',context)


class ProjectView(View):
    def work_unit(self,request,work_unit_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['work_unit']=WorkUnitRepo(user=user).work_unit(work_unit_id=work_unit_id)
        return render(request,TEMPLATE_ROOT+'work_unit.html',context)

    def project(self,request,project_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['project']=ProjectRepo(user=user).project(project_id=project_id)
        return render(request,TEMPLATE_ROOT+'project.html',context)
