from django.shortcuts import render,redirect
from .forms import *
from app.forms import AddTagForm
from app.serializers import TagSerializer
from django.views import View
from app.repo import ProfileRepo
from app.constants import SUCCEED,FAILED
from django.http import Http404,JsonResponse
from app.views import getContext as AppContext
from .enums import MaterialRequestStatusEnum,IssueTypeEnum
from .repo import MaterialBrandRepo,MaterialObjectRepo,MaterialWareHouseRepo,ContractorRepo,AssignmentRepo,IssueRepo,ProjectRepo,MaterialCategoryRepo,ProjectCategoryRepo,WorkUnitRepo,ManagerPageRepo,MaterialRepo,MaterialRequestRepo
from .apps import APP_NAME
from app.repo import TagRepo
import json
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
        context['material_categories']=MaterialCategoryRepo(user=user).list_root()
        # context['projects']=ProjectRepo(user=user).get_roots()
        return render(request,TEMPLATE_ROOT+'index.html',context)
    
    def chart(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)        
        context['work_units']=WorkUnitRepo(user=user).get_roots()
        return render(request,TEMPLATE_ROOT+'chart.html',context)
 

    def resume(self,request):
        context=getContext(request)
        context['count']=[{},{},{}]
        return render(request,TEMPLATE_ROOT+'resume.html',context)  
    def search(self,request,*args, **kwargs):
        user=request.user
        if request.method=='POST':
            search_form=SearchForm(request.POST)
            if search_form.is_valid():
                search_for=search_form.cleaned_data['search_for']
                context=getContext(request)
                context['pages']=ManagerPageRepo(user=user).search(search_for=search_for)
                context['search_for']=search_for
                cont_repo=ContractorRepo(user=user)
                context['contractors']=cont_repo.search(search_for=search_for)
                context['profiles']=ProfileRepo(user=user).search(search_for=search_for)
                context['materialobjects']=MaterialObjectRepo(user=user).search(search_for=search_for)
                
                return render(request,TEMPLATE_ROOT+'search.html',context)

class ManagerPageView(View):
    def get_page_context(self,request,*args, **kwargs):
        user=request.user
        context=getContext(request)
        if user and user.is_authenticated and user.has_perm(APP_NAME+'.add_issue'):
            context['add_issue_form']=AddIssueForm()
            context['issue_types']=list(x.value for x in IssueTypeEnum)
        
        if user.has_perm(APP_NAME+'.add_document'):
            context['add_document_form']=AddDocumentForm()
        if user.has_perm(APP_NAME+'.add_link'):
            context['add_link_form']=AddLinkForm()
        if user.has_perm('app.add_tag'):
            context['add_tag_form']=AddTagForm()
        return context

    def page(self,request,page_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        page=ManagerPageRepo(user=user).page(page_id=page_id)
        context['page']=page        
        return render(request,TEMPLATE_ROOT+'page.html',context) 
    
    def assignment(self,request,assignment_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        assignment=AssignmentRepo(user=user).assignment(assignment_id=assignment_id)
        context['page']=assignment        
        return render(request,TEMPLATE_ROOT+'page.html',context) 
    
    def add_material(self,request,*args, **kwargs):
        if request.method=='POST':
            add_material_form=AddMaterialForm(request.POST)
            if add_material_form.is_valid():
                # print(ssssssssss)
                title=add_material_form.cleaned_data['title']
                category_id=add_material_form.cleaned_data['category_id']
                material=MaterialRepo(user=request.user).add(title=title,category_id=category_id)
                if material is not None:
                    return redirect(material.category.get_absolute_url())
    def add_material_category(self,request,*args, **kwargs):
        if request.method=='POST':
            add_material_category_form=AddMaterialCategoryForm(request.POST)
            if add_material_category_form.is_valid():
                title=add_material_category_form.cleaned_data['title']
                parent_id=add_material_category_form.cleaned_data['parent_id']
                material_category=MaterialCategoryRepo(user=request.user).add(title=title,parent_id=parent_id)
                if material_category is not None:
                    return redirect(material_category.parent.get_absolute_url())

               
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

    def material_request(self,request,material_request_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
      
        if user and user.is_authenticated:
            context['sign_material_request_form']=SignMaterialRequestForm()
            context['status_options']=list(x.value for x in MaterialRequestStatusEnum)
        material_request=MaterialRequestRepo(user=user).material_request(material_request_id=material_request_id)
        context['material_request']=material_request
        return render(request,TEMPLATE_ROOT+'material-request.html',context)
    
    def material(self,request,material_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        material=MaterialRepo(user=user).material(material_id=material_id)
        context['material']=material
        context['projects']=ProjectRepo(user=user).my_projects()
        context['add_metrial_request_form']=AddMaterialRequestForm()
        context['unit_names']=['عدد','کیلو','دستگاه']
        return render(request,TEMPLATE_ROOT+'material.html',context)
    
    def materialbrand(self,request,materialbrand_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        materialbrand=MaterialBrandRepo(user=user).materialbrand(materialbrand_id=materialbrand_id)
        
        context['page']=materialbrand
        context['materialbrand']=materialbrand
        return render(request,TEMPLATE_ROOT+'materialbrand.html',context)
    
    def materialobject(self,request,materialobject_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        materialobject=MaterialObjectRepo(user=user).materialobject(materialobject_id=materialobject_id)
        
        
        context['materialobject']=materialobject
        context['material']=materialobject.material
        return render(request,TEMPLATE_ROOT+'materialobject.html',context)
    
    def materialwarehouse(self,request,materialwarehouse_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        material_warehouse=MaterialWareHouseRepo(user=user).materialwarehouse(materialwarehouse_id=materialwarehouse_id)
        
         
        materials=[]
        context['page']=material_warehouse
        context['warehouse']=material_warehouse

        context['materials']=material_warehouse.materials()
        context['materials2']=material_warehouse.materials2()
        # print(materials)
        return render(request,TEMPLATE_ROOT+'warehouse.html',context)
    
    def category(self,request,category_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        
        category=MaterialCategoryRepo(user=user).category(category_id=category_id)
        context['category']=category   
        if user.has_perm(APP_NAME+'.add_material'):
            context['add_material_form']=AddMaterialForm()
        if user.has_perm(APP_NAME+'.add_materialcategory'):
            context['add_material_category_form']=AddMaterialCategoryForm()
        return render(request,TEMPLATE_ROOT+'material-category.html',context)

    def add_tag(self,request,*args, **kwargs):
        if request.method=='POST':
            add_tag_form=AddTagForm(request.POST,request.FILES)
            if add_tag_form.is_valid():  
                tag_title=add_tag_form.cleaned_data['tag_title']
                page_id=add_tag_form.cleaned_data['page_id']     
                tag=ManagerPageRepo(user=request.user).add_tag(tag_title=tag_title,page_id=page_id)
                if tag is not None:
                    page=ManagerPageRepo(user=request.user).page(page_id=page_id)
                    tags=page.tags.all()
                    return JsonResponse({'result':SUCCEED,'tag':TagSerializer(tag).data}) 
                    # return JsonResponse({'result':SUCCEED,'tags':TagSerializer(tags,many=True).data}) 
            return JsonResponse({'result':FAILED})
    
    def add_link(self,request,*args, **kwargs):
        if request.method=='POST':
            add_link_form=AddLinkForm(request.POST)
            if add_link_form.is_valid():
                title=add_link_form.cleaned_data['title']
                manager_page_id=add_link_form.cleaned_data['manager_page_id']
                added=ManagerPageRepo(user=request.user).add_link(title=title,manager_page_id=manager_page_id)
                if added:
                    page=ManagerPageRepo(user=request.user).get(pk=manager_page_id)
                    return redirect(page.get_absolute_url())
        return Http404      
        
    def add_document(self,request,*args, **kwargs):
        if request.method=='POST':
            add_document_form=AddDocumentForm(request.POST)
            if add_document_form.is_valid():
                title=add_document_form.cleaned_data['title']
                manager_page_id=add_document_form.cleaned_data['manager_page_id']
                added=ManagerPageRepo(user=request.user).add_document(title=title,manager_page_id=manager_page_id)
                if added:                    
                    page=ManagerPageRepo(user=request.user).get(pk=manager_page_id)
                    return redirect(page.get_absolute_url())
        return Http404      

    def work_unit(self,request,work_unit_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        work_unit=WorkUnitRepo(user=user).work_unit(work_unit_id=work_unit_id)
        page=work_unit
        context['page']=page
        context['workunit_workunits']=work_unit.childs()
        context['workunit_projects']=work_unit.project_set.all()
        context['work_unit']=WorkUnitRepo(user=user).work_unit(work_unit_id=work_unit_id)
        return render(request,TEMPLATE_ROOT+'page.html',context)

    def add_issue(self,request,*args, **kwargs):
        if request.method=='POST':
            add_issue_form=AddIssueForm(request.POST)
            if add_issue_form.is_valid():
                issue_type=add_issue_form.cleaned_data['issue_type']
                title=add_issue_form.cleaned_data['title']
                page_id=add_issue_form.cleaned_data['page_id']
                issue=IssueRepo(user=request.user).add(issue_type=issue_type,title=title,page_id=page_id)
                if issue is not None:
                    return redirect(issue.page.get_absolute_url())
        return Http404      

    def project(self,request,project_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        page=ProjectRepo(user=user).project(project_id=project_id)
        project=ProjectRepo(user=user).project(project_id=project_id)
        context['page']=project
        context['project_projects']=project.childs()
        context['project']=project
        
        # context['contractors']=project.contractors.all()
        context['tags_s']=json.dumps(TagSerializer(page.tags.all(),many=True).data)
        return render(request,TEMPLATE_ROOT+'page.html',context)
    
    def project_avo(self,request,project_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        page=ProjectRepo(user=user).project(project_id=project_id)
        project=ProjectRepo(user=user).project(project_id=project_id)
        context['page']=project
        context['project_projects']=project.childs()
        context['project']=project
        
        context['tags_s']=json.dumps(TagSerializer(page.tags.all(),many=True).data)
        return render(request,'avo/page.html',context)

    def issue(self,request,issue_id,*args, **kwargs):
        user=request.user
        context=self.get_page_context(request)
        
        context['page']=IssueRepo(user=user).issue(issue_id=issue_id)
        return render(request,TEMPLATE_ROOT+'issue.html',context)

    def tag(self,request,tag_id,*args,**kwargs):
        user=request.user

        context=getContext(request=request)
        
        tag=TagRepo(user=user).get(tag_id=tag_id)    
        
        
        
        context['pages']=ManagerPageRepo(user=request.user).list_by_tag(tag_id=tag_id)
        return render(request,TEMPLATE_ROOT+'search.html',context)