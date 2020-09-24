from django.shortcuts import render,redirect,reverse
from .forms import *
from django.views import View
from django.http import Http404
from app.views import getContext as AppContext
from .repo import ProjectRepo,ProjectCategoryRepo
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
        return render(request,TEMPLATE_ROOT+'index.html',context)
 
        
    def search(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['project_categories']=ProjectCategoryRepo(user=user).list()
        context['projects']=ProjectRepo(user=user).list()
        return render(request,TEMPLATE_ROOT+'search.html',context)


class ProjectView(View):
    def project(self,request,project_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['page']=ProjectRepo(user=user).project(project_id=project_id)
        return render(request,TEMPLATE_ROOT+'page.html',context)

