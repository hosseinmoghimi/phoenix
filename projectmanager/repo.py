
from .models import ProjectCategory,Project,WorkUnit,Employee,Material,MaterialObject,MaterialWareHouse,MaterialCategory
from app.repo import ProfileRepo
from django.contrib.auth.models import Group
class EmployeeRepo:
    def __init__(self,user):
        self.objects=Employee.objects
        self.user=user
        self.profile=ProfileRepo(user=user).me
        if self.profile is None:
            self.me=None
        else:
            try:
                self.employee=self.objects.get(profile=self.profile)
            except:
                self.employee=None
    




class ProjectRepo:
    def __init__(self,user=None):
        self.objects=Project.objects
        self.user=user
    def list(self):
        return self.objects.all()
    def project(self,project_id):
        try:
            return self.objects.get(pk=project_id)
        except:
            return None
    def get(self,project_id):
            return self.project(project_id=project_id)



class WorkUnitRepo:
    def __init__(self,user=None):
        self.objects=WorkUnit.objects
        self.user=user
    def list(self):
        return self.objects.all()
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