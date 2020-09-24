
from .models import ProjectCategory,Project,WorkUnit,Employee,Material,MaterialObject,MaterialWareHouse,MaterialCategory
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