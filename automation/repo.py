from .models import Project,WorkUnit,ProductRequest,ProductRequestSignature,Employee
from .apps import APP_NAME
from app.repo import ProfileRepo
from app.repo import SignatureRepo
from market.repo import ProductRepo
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
    


class EmployeeRepo:
    def my_employees(self):
        return Employee.objects.filter(profile=self.profile)
    def __init__(self,user=None):
        self.user=user
        self.objects=Employee.objects
        self.profile=ProfileRepo(user=user).me
        try:
            self.me=self.objects.filter(profile=self.profile).first()
        except:
            self.me=None
        try:
            self.me = self.objects.get(profile=self.profile)          
        except :
            self.me = None
    def list(self):
        return self.objects.all()
        
    def get(self,employee_id):
        try:
            return self.objects.get(pk=employee_id)
        except :
            return None



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
    def add(self,product_id,product_unit,quantity,work_unit_id):
        employee=EmployeeRepo(user=self.user).me  
        work_unit=WorkUnitRepo(user=self.user).work_unit(work_unit_id=work_unit_id)  
        product=ProductRepo(user=self.user).get(product_id=product_id)  
        if employee is not None and product is not None and work_unit is not None:   
            product_request=ProductRequest(employee=employee,product=product,product_unit=product_unit,quantity=quantity,work_unit=work_unit)
            product_request.save()
            return product_request
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
                product_request.status=status
                product_request.save()
                return product_request
            