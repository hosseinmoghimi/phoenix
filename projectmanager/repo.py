
from .models import MaterialBrand,MaterialObject,Contractor,MaterialWareHouse,Assignment,Issue,MaterialRequest,ManagerPage,ProjectCategory,Project,WorkUnit,Employee,Material,MaterialObject,MaterialWareHouse,MaterialCategory
from app.repo import ProfileRepo,SignatureRepo,TagRepo
from django.contrib.auth.models import Group
from django.db.models import Q
from app.models import Link,Document,Tag
from .apps import APP_NAME
import datetime

class ContractorRepo:
    def __init__(self,user=None):
        self.objects=Contractor.objects   
        self.user=user
        self.profile=ProfileRepo(user=user).me
        self.me=None
        try:
            if self.profile is not None:
                self.me=self.objects.get(profile=self.profile)
        except:
            pass
       


    def search(self,search_for):
        return self.objects.filter(title__contains=search_for)

class AssignmentRepo:
    def __init__(self,user):
        self.user=user
        self.objects=Assignment.objects
    def assignment(self,assignment_id):
        try:
            return self.objects.get(pk=assignment_id)
        except:
            return None
            

class EmployeeRepo:
    def __init__(self,user):
        self.objects=Employee.objects
        self.user=user
        self.profile=ProfileRepo(user=user).me
        self.me=None
        #must be deleted
        # print('self.profile')
        # print(self.profile)
        if self.profile is None:
            self.me=None
        else:
            try:
                self.me=self.objects.get(profile=self.profile)
            except:
                self.me=None
    

    def search(self,search_for):
        profiles = ProfileRepo(user=self.user).search(search_for=search_for)
        return profiles

class ManagerPageRepo:
    def add_tag(self,tag_title,page_id):
        page=self.page(page_id=page_id)
        if tag_title in list(tag.title for tag in page.tags.all()):
            return None
        tag=None
        try:
            tag=Tag.objects.get(title=tag_title)
        except:
            tag=Tag(title=tag_title)
            tag.save()
        if page is not None and tag is not None:
            page.tags.add(tag)
            return tag
        return tag
                
    def search(self,search_for):
        return self.objects.filter(
            Q(title__contains=search_for) | 
            Q(pretitle__contains=search_for)| 
            Q(posttitle__contains=search_for)| 
            Q(description__contains=search_for)
            )
    def add_link(self,title,manager_page_id):
        manager_page=self.page(page_id=manager_page_id)
        if manager_page is not None and self.user and self.user.has_perm(APP_NAME+'.add_link'):
            profile=ProfileRepo(user=self.user).me
            if profile is not None:
                link=Link(title=title,icon_material='link',profile=profile)
                link.save()
                manager_page.links.add(link)
            return True 
        return False
    def add_document(self,title,manager_page_id):
        manager_page=self.page(page_id=manager_page_id)
        if manager_page is not None and self.user and self.user.has_perm(APP_NAME+'.add_link'):
            profile=ProfileRepo(user=self.user).me
            if profile is not None:
                document=Document(title=title,icon_material='get_app',profile=profile)  
                document.save()              
                manager_page.documents.add(document) 
            return True
        return False

    def add_location(self,page_id,location):
        if self.user.has_perm(APP_NAME+'.change_managerpage'):
            page=self.get(pk=page_id)
            if page is not None:
                location=location
                location=location.replace('width="600"','width="100%"')
                location=location.replace('height="450"','height="500"')
                page.location=location
                page.save()
                return page

                
                
    def __init__(self,user):
        self.objects=ManagerPage.objects
        self.user=user
    def priority(self,base_class,direction,pk):
        if base_class=='project':
            self.objects=ProjectRepo(user=self.user).objects.filter(parent=None)
        if direction=='down':
            self.go_down(pk)
        if direction=='up':
            self.go_up(pk)
    
    def page(self,page_id):
        try:
            return self.objects.get(pk=page_id)
        except:
            return None
    def get(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None
    def go_up(self,pk):
        down_object=self.get(pk=pk)   
        if down_object is  not None:
            down_priority=down_object.priority
            try:
                up_object=self.objects.filter(priority__gt=down_priority).order_by('priority').first()
                up_priority=up_object.priority
            except:
                up_object=None
            if up_object is not None:
                down_object.priority=up_priority
                down_object.save()
                up_object.priority=down_priority
                up_object.save()
                # print('up_object')
                # print(up_object)     
                # print('down_object')
                # print(down_object)

    def go_down(self,pk):
        up_object=self.get(pk=pk)
        if up_object is not None:
            up_priority=up_object.priority
            try:
                down_object=self.objects.filter(priority__lt=up_priority).order_by('-priority').first()
           
                down_priority=down_object.priority

            except:
                down_object=None
            if down_object is not None:
                up_object.priority=down_priority
                up_object.save()
                down_object.priority=up_priority
                down_object.save()
                # print('up_object')
                # print(up_object)     
                # print('down_object')
                # print(down_object)

    def list_by_tag(self,tag_id):
        tag=TagRepo(user=self.user).tag(tag_id=tag_id)
        if tag is not None:
            return tag.managerpage_set.all()

class MaterialRequestRepo:
    def __init__(self,user):
        self.user=user
        self.objects=MaterialRequest.objects
    def material_request(self,material_request_id):
        try:
            return self.objects.get(pk=material_request_id)
        except:
            return None            
    def add(self,unit_name,quantity,project_id,material_id):
        user=self.user
        contractor=ContractorRepo(user=user).me
        employee=EmployeeRepo(user=user).me
        material=MaterialRepo(user=user).material(material_id=material_id)
        project=ProjectRepo(user=user).project(project_id=project_id)
        if project is not None and material is not None and (employee is not None or contractor is not None):
            title=f'درخواست {quantity} {unit_name} " {material.title} " برای پروژه {project.title}'
            material_request=MaterialRequest(title=title,requested_material=material,unit_name=unit_name,quantity=quantity,for_project=project,contractor=contractor,employee=employee)
            material_request.save()
            if material_request is not None:
                return material_request

    def sign(self,description,status,material_request_id):
        if self.user and self.user is not None and self.user.is_authenticated:
            signature=SignatureRepo(user=self.user).add(status=status,description=description)
            if signature is not None:
                material_request=self.material_request(material_request_id=material_request_id)
                # product_request_signature=ProductRequestSignature(signature=signature,status=status)
                signature.save()
                material_request.signatures.add(signature)
                # material_request.status=status
                # material_request.save()
                return material_request

                      

class ProjectRepo:
    def __init__(self,user=None):
        self.objects=Project.objects
        self.user=user
        self.profile=ProfileRepo(user=self.user).me
        self.me_employee=EmployeeRepo(user=self.user).me
        self.me_contractor=ContractorRepo(user=self.user).me
        #must be deleted
        # print('me_employee')
        # print(self.me_employee)
        # print('me_contractor')
        # print(self.me_contractor)
    def my_projects(self):
        if self.me_contractor is not None:
            return self.me_contractor.project_set.all()
        if self.me_employee is not None:
            return self.me_employee.work_unit.project_set.all()
    def list(self):
        return self.objects.order_by('-priority')
    def get_roots(self):
        return self.objects.filter(parent=None)
    def project(self,project_id):
        try:
            return self.objects.get(pk=project_id)
        except:
            return None
    def get(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None
    def go_up(self,pk):
        down_object=self.get(pk=pk)
        try:
            up_object=self.objects.get(priority=down_object.priority)
        except:
            up_object=None
        if down_object is not None:
            down_object.priority=down_object.priority+1
            down_object.save()
        if up_object is not None:
            up_object.priority=up_object.priority-1
            up_object.save()

    def go_down(self,pk):
        up_object=self.get(pk=pk)
        try:
            down_object=self.objects.get(priority=down_object.priority)
        except:
            down_object=None
        if down_object is not None:
            down_object.priority=down_object.priority-1
            down_object.save()
        if up_object is not None:
            up_object.priority=up_object.priority+1
            up_object.save()

    def add(self,title,parent_id):
        parent=self.project(project_id=parent_id)
        project=Project(color='primary',parent=parent,icon='construction',title=title)
        project.save()
        if project is not None:
            return project
             
              

class IssueRepo:
    def __init__(self,user=None):
        self.objects=Issue.objects
        self.user=user
    def add(self,issue_type,title,page_id):
        date_report=datetime.datetime.now()
        issue=Issue(date_report=date_report,color='danger',page_id=page_id,icon='report_problem',title=title,issue_type=issue_type)
        issue.save()
        if issue is not None:
            return issue

                
    def list(self):
        return self.objects.order_by('-priority')
    
    def issue(self,issue_id):
        try:
            return self.objects.get(pk=issue_id)
        except:
            return None 

class MaterialRepo:
    def __init__(self,user=None):
        self.objects=Material.objects
        self.user=user
    def list(self):
        return self.objects.order_by('-priority')
    
    def material(self,material_id):
        try:
            return self.objects.get(pk=material_id)
        except:
            return None
    def get(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None
    
    def add(self,title,category_id):
        if self.user.has_perm(APP_NAME+'.add_material'):
            category=MaterialCategoryRepo(user=self.user).material_category(material_category_id=category_id)
            if category is None:
                return None
            material=Material(title=title,category=category)
            material.save()
            return material
              

class MaterialWareHouseRepo:
    def __init__(self,user=None):
        self.objects=MaterialWareHouse.objects
        self.user=user
    def list(self):
        return self.objects.order_by('-priority')
    
    def materialwarehouse(self,materialwarehouse_id):
        try:
            return self.objects.get(pk=materialwarehouse_id)
        except:
            return None
    def get(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None
    
    
class MaterialCategoryRepo:
    def __init__(self,user=None):
        self.objects=MaterialCategory.objects
        self.user=user
    def list(self):
        return self.objects.order_by('-priority')
    def list_root(self):
        return self.objects.filter(parent=None).order_by('-priority')
    
    def material_category(self,material_category_id):
        try:
            return self.objects.get(pk=material_category_id)
        except:
            return None
    def category(self,category_id):
        try:
            return self.objects.get(pk=category_id)
        except:
            return None
    def get(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None
    
    def add(self,title,parent_id):
        if self.user.has_perm(APP_NAME+'.add_material'):
            parent=MaterialCategoryRepo(user=self.user).material_category(material_category_id=parent_id)
            if parent is None:
                return None
            material_category=MaterialCategory(title=title,parent=parent)
            material_category.save()
            return material_category

class WorkUnitRepo:
    def __init__(self,user=None):
        self.objects=WorkUnit.objects
        self.user=user
    def list(self):
        return self.objects.all()
    def get_roots(self):
        return self.objects.filter(parent=None)
    def work_unit(self,work_unit_id):
        try:
            return self.objects.get(pk=work_unit_id)
        except:
            return None
    def get(self,work_unit_id):
            return self.project(work_unit_id=work_unit_id)
    def add(self,title,parent_id):
        parent=self.work_unit(work_unit_id=parent_id)
        work_unit=WorkUnit(color='primary',parent=parent,icon='apartment',title=title)
        work_unit.save()
        if work_unit is not None:
            return work_unit
class MaterialObjectRepo:
    def __init__(self,user=None):
        self.objects=MaterialObject.objects
        self.user=user
    def list(self):
        return self.objects.all()
    def get(self,materialobject_id):
            try:
                return self.objects.get(pk=materialobject_id)
            except:
                return None
    def materialobject(self,materialobject_id):
            return self.get(materialobject_id=materialobject_id)
    def search(self,search_for):
        return self.objects.filter(serial_no__contains=search_for)

class MaterialBrandRepo:
    def __init__(self,user=None):
        self.objects=MaterialBrand.objects
        self.user=user
    def list(self):
        return self.objects.all()
    def get(self,materialbrand_id):
            try:
                return self.objects.get(pk=materialbrand_id)
            except:
                return None
    def materialbrand(self,materialbrand_id):
            return self.get(materialbrand_id=materialbrand_id)


class ProjectCategoryRepo:
    def __init__(self,user=None):
        self.objects=ProjectCategory.objects
        self.user=user
    def list(self):
        return self.objects.all()
    def get(self,project_id):
        try:
            return self.objects.get(pk=project_id)
        except:
            return None