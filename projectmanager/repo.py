
from .models import MaterialRequest,Contractor,ManagerPage,ProjectCategory,Project,WorkUnit,Employee,Material,MaterialObject,MaterialWareHouse,MaterialCategory
from app.repo import ProfileRepo
from django.contrib.auth.models import Group
class EmployeeRepo:
    def __init__(self,user):
        self.objects=Employee.objects
        self.user=user
        self.profile=ProfileRepo(user=user).me
        self.me=None
        #must be deleted
        print('self.profile')
        print(self.profile)
        if self.profile is None:
            self.me=None
        else:
            try:
                self.me=self.objects.get(profile=self.profile)
            except:
                self.me=None
    


class ManagerPageRepo:
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



class MaterialRequestRepo:
    def __init__(self,user):
        self.user=user
        self.objects=MaterialRequest.objects
    def add(self,unit_name,quantity,project_id,material_id):
        user=self.user
        contractor=ContractorRepo(user=user).me
        employee=EmployeeRepo(user=user).me
        material=MaterialRepo(user=user).material(material_id=material_id)
        project=ProjectRepo(user=user).project(project_id=project_id)
        if project is not None and material is not None and (employee is not None or contractor is not None):
            material_request=MaterialRequest(requested_material=material,unit_name=unit_name,quantity=quantity,for_project=project,contractor=contractor,employee=employee)
            material_request.save()
            if material_request is not None:
                return material_request

                

class ContractorRepo:
    def __init__(self,user):
        self.objects=Contractor.objects   
        self.user=user
        self.profile=ProfileRepo(user=user).me
        self.me=None
        try:
            if self.profile is not None:
                self.me=self.objects.get(profile=self.profile)
        except:
            pass
       

class ProjectRepo:
    def __init__(self,user=None):
        self.objects=Project.objects
        self.user=user
        self.profile=ProfileRepo(user=self.user).me
        self.me_employee=EmployeeRepo(user=self.user).me
        self.me_contractor=ContractorRepo(user=self.user).me
        print('me_employee')
        print(self.me_employee)
        print('me_contractor')
        print(self.me_contractor)
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