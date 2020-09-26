from django.shortcuts import render,redirect
from .forms import *
from django.views import View
from django.http import Http404
from app.views import getContext as AppContext
from .enums import MaterialRequestStatusEnum
from .repo import IssueRepo,ProjectRepo,MaterialCategoryRepo,ProjectCategoryRepo,WorkUnitRepo,ManagerPageRepo,MaterialRepo,MaterialRequestRepo
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
    def page(self,request,page_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        page=ManagerPageRepo(user=user).page(page_id=page_id)
        context['page']=page        
        return render(request,TEMPLATE_ROOT+'page.html',context)
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
        context['material_categories']=MaterialCategoryRepo(user=user).list_root()
        context['projects']=ProjectRepo(user=user).get_roots()
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def chart(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)        
        context['work_units']=WorkUnitRepo(user=user).get_roots()
        return render(request,TEMPLATE_ROOT+'chart2.html',context)
 
        
    def search(self,request,*args, **kwargs):
        user=request.user
        if request.method=='POST':
            search_form=SearchForm(request.POST)
            if search_form.is_valid():
                search_for=search_form.cleaned_data['search_for']
                context=getContext(request)
                context['pages']=ManagerPageRepo(user=user).search(search_for=search_for)
                context['search_for']=search_for
                return render(request,TEMPLATE_ROOT+'search.html',context)

class MaterialView(View):
    def material(self,request,material_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        material=MaterialRepo(user=user).material(material_id=material_id)
        context['material']=material
        context['projects']=ProjectRepo(user=user).my_projects()
        context['add_metrial_request_form']=AddMaterialRequestForm()
        context['unit_names']=['عدد','کیلو','دستگاه']
        return render(request,TEMPLATE_ROOT+'material.html',context)
    def category(self,request,category_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        category=MaterialCategoryRepo(user=user).category(category_id=category_id)
        context['category']=category        
        return render(request,TEMPLATE_ROOT+'material-category.html',context)

class MaterialRequestView(View):
    def material_request(self,request,material_request_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        if user and user.is_authenticated:
            context['sign_material_request_form']=SignMaterialRequestForm()
            context['status_options']=list(x.value for x in MaterialRequestStatusEnum)
        material_request=MaterialRequestRepo(user=user).material_request(material_request_id=material_request_id)
        context['material_request']=material_request
        return render(request,TEMPLATE_ROOT+'material-request.html',context)
    def sign(self,request,*args, **kwargs):
        if request.method=='POST':
            sign_material_request_form=SignMaterialRequestForm(request.POST)
            if sign_material_request_form.is_valid():
                material_request_id=sign_material_request_form.cleaned_data['material_request_id']
                status=sign_material_request_form.cleaned_data['status']
                description=sign_material_request_form.cleaned_data['description']
                
                user=request.user
                material_request=MaterialRequestRepo(user=user).sign(description=description,status=status,material_request_id=material_request_id)
                
                if material_request is not None:
                    return redirect(material_request.get_absolute_url())
        return Http404

    def add_material_request(self,request):
        if request.method=='POST':
            add_material_request=AddMaterialRequestForm(request.POST)
            if add_material_request.is_valid():
                project_id=add_material_request.cleaned_data['project_id']
                material_id=add_material_request.cleaned_data['material_id']
                quantity=add_material_request.cleaned_data['quantity']
                unit_name=add_material_request.cleaned_data['unit_name']
                material_request=MaterialRequestRepo(user=request.user).add(unit_name=unit_name,quantity=quantity,project_id=project_id,material_id=material_id)
                if material_request is not None:
                    return redirect(reverse('projectmanager:project',kwargs={'project_id':project_id}))
                else:
                    return redirect(reverse('projectmanager:material',kwargs={'material_id':material_id}))



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


    def issue(self,request,issue_id,*args, **kwargs):
        user=request.user
        context=getContext(request)
        context['issue']=IssueRepo(user=user).issue(issue_id=issue_id)
        return render(request,TEMPLATE_ROOT+'issue.html',context)

