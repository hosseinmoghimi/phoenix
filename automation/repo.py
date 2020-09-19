from .models import Project,WorkUnit,ProductRequest
from .apps import APP_NAME
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
    def add(self,project_id,title):
        user=self.user
        if self.user.has_perm(f'{APP_NAME}.add_workunit'):
            work_unit=WorkUnit(title=title)
            project=ProjectRepo(user=self.user).project(project_id=project_id)
            if project is not None:
                work_unit.save()
                project.work_units.add(work_unit)
                return work_unit
    


class ProjectRepo:
    def __init__(self,user=None):
        self.objects=Project.objects
    def list(self):
        return self.objects.all()
    def project(self,project_id):
        try:
            return self.objects.get(pk=project_id)
        except:
            return None

class ProductRequestRepo:
    def __init__(self,user=None):
        self.objects=ProductRequest.objects
    def list(self):
        return self.objects.all()
    def product_request(self,product_request_id):
        try:
            return self.objects.get(pk=product_request_id)
        except:
            return None
    def list_for_work_unit(self,work_unit_id):
        return self.objects.filter(work_unit_id=work_unit_id)