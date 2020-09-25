from django.shortcuts import render,redirect,reverse
from .forms import *
from django.views import View
from django.http import Http404
from app.views import getContext as AppContext
from .repo import ProjectRepo,ProjectCategoryRepo,WorkUnitRepo,ManagerPageRepo,MaterialRepo
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
    def priority(self,request,*args, **kwargs):
        if request.method=='POST':
            priority_form=PriorityForm(request.POST)
            if priority_form.is_valid():
                base_class=priority_form.cleaned_data['base_class']
                direction=priority_form.cleaned_data['direction']
                pk=priority_form.cleaned_data['pk']
                ManagerPageRepo(user=request.user).priority(base_class=base_class,direction=direction,pk=pk)
        return redirect(reverse('projectmanager:home'))       
    def home(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['priority_form']=PriorityForm()
        context['project_categories']=ProjectCategoryRepo(user=user).list()
        context['projects']=ProjectRepo(user=user).get_roots()
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def chart(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)        
        context['work_units']=WorkUnitRepo(user=user).get_roots()
        return render(request,TEMPLATE_ROOT+'chart.html',context)
 
        
    def search(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['project_categories']=ProjectCategoryRepo(user=user).list()
        context['projects']=ProjectRepo(user=user).list()
        return render(request,TEMPLATE_ROOT+'search.html',context)
class MaterialView(View):
    def material(self,request,material_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['material']=MaterialRepo(user=user).material(material_id=material_id)
        return render(request,TEMPLATE_ROOT+'material.html',context)



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

