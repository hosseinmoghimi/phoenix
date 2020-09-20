from .models import Project,WorkUnit,ProductRequest,ProductRequestSignature
from .apps import APP_NAME
from app.repo import ProfileRepo
from app.repo import SignatureRepo
class WorkUnitRepo:
    def __init__(self,user=None):
        self.objects=WorkUnit.objects
        self.user=user
        self.profile=ProfileRepo(user=user).me
    def my_work_units(self):
        return self.profile.employee_set.all()
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
        self.user=user
    def list(self):
        return self.objects.all()
    def project(self,project_id):
        try:
            return self.objects.get(pk=project_id)
        except:
            return None

class ProductRequestRepo:
    def __init__(self,user=None):
        self.user=user
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
    def sign(self,product_request_id,status,description):
        if self.user.is_authenticated:
            signature=SignatureRepo(user=self.user).add(description=description)
            if signature is not None:
                product_request=self.product_request(product_request_id=product_request_id)
                product_request_signature=ProductRequestSignature(signature=signature,status=status)
                product_request_signature.save()
                product_request.signatures.add(product_request_signature)
                return product_request
            