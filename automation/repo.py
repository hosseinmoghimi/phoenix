from .models import WorkUnit,ProductRequest

class WorkUnitRepo:
    def __init__(self,user=None):
        self.objects=WorkUnit.objects
    def list(self):
        return self.objects.all()
    def work_unit(self,work_unit_id):
        try:
            return self.objects.get(pk=work_unit_id)
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